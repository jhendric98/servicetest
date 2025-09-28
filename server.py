"""Flask RESTful API exposing a subset of the Chinook database."""

from __future__ import annotations

import argparse
from http import HTTPStatus
from typing import Any, Callable, Dict, Iterable, Mapping, MutableMapping

from flask import Flask, current_app, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from yahoo_fin import stock_info


EmployeePayload = MutableMapping[str, Any]
QuoteFetcher = Callable[[str], Mapping[str, Any]]


EMPLOYEE_FIELDS = {
    "Address",
    "BirthDate",
    "City",
    "Country",
    "Email",
    "Fax",
    "FirstName",
    "HireDate",
    "LastName",
    "Phone",
    "PostalCode",
    "ReportsTo",
    "State",
    "Title",
}

REQUIRED_EMPLOYEE_FIELDS = {
    "LastName",
    "FirstName",
    "Title",
    "Address",
    "City",
    "Country",
    "Phone",
    "Email",
}


def _row_to_dict(rows: Iterable[Mapping[str, Any]]) -> list[Dict[str, Any]]:
    """Return a JSON serialisable representation for SQLAlchemy rows."""

    return [dict(row) for row in rows]


def default_quote_fetcher(ticker: str) -> Mapping[str, Any]:
    """Fetch quote data for *ticker* using :mod:`yahoo_fin`."""

    return stock_info.get_quote_table(ticker)


def _get_engine() -> Engine:
    engine: Engine = current_app.config["DB_ENGINE"]
    return engine


class Employees(Resource):
    """Resource providing read/write access to employees."""

    def get(self) -> Any:
        engine = _get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM employees"))
            employees = _row_to_dict(result.mappings())
        return jsonify({"employees": employees})

    def post(self) -> Any:
        payload: EmployeePayload | None = request.get_json(silent=True)
        if not payload:
            return {"message": "Request body must be valid JSON."}, HTTPStatus.BAD_REQUEST

        unknown = set(payload) - EMPLOYEE_FIELDS
        if unknown:
            return {
                "message": "Request contained unsupported fields.",
                "fields": sorted(unknown),
            }, HTTPStatus.BAD_REQUEST

        missing = REQUIRED_EMPLOYEE_FIELDS - payload.keys()
        if missing:
            return {
                "message": "Missing required fields.",
                "fields": sorted(missing),
            }, HTTPStatus.BAD_REQUEST

        engine = _get_engine()
        insert_stmt = text(
            """
            INSERT INTO employees (
                LastName, FirstName, Title, ReportsTo, BirthDate, HireDate,
                Address, City, State, Country, PostalCode, Phone, Fax, Email
            )
            VALUES (
                :LastName, :FirstName, :Title, :ReportsTo, :BirthDate, :HireDate,
                :Address, :City, :State, :Country, :PostalCode, :Phone, :Fax, :Email
            )
            """
        )

        try:
            employee_payload = {field: payload.get(field) for field in EMPLOYEE_FIELDS}
            with engine.begin() as conn:
                result = conn.execute(insert_stmt, parameters=employee_payload)
                employee_id = result.lastrowid
                inserted = conn.execute(
                    text("SELECT * FROM employees WHERE EmployeeId = :employee_id"),
                    {"employee_id": employee_id},
                ).mappings()
                employee = dict(next(inserted))
        except (SQLAlchemyError, StopIteration) as exc:  # pragma: no cover - defensive
            current_app.logger.exception("Failed to insert employee")
            return {"message": "Could not store employee.", "details": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return employee, HTTPStatus.CREATED


class Tracks(Resource):
    """Resource providing read-only access to track metadata."""

    def get(self) -> Any:
        engine = _get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT TrackId, Name, Composer, UnitPrice FROM tracks ORDER BY TrackId")
            )
            tracks = _row_to_dict(result.mappings())
        return jsonify({"data": tracks})


class Employee(Resource):
    """Resource returning a single employee by id."""

    def get(self, employee_id: int) -> Any:
        engine = _get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM employees WHERE EmployeeId = :employee_id"),
                {"employee_id": employee_id},
            ).mappings()
            employee = result.first()

        if employee is None:
            return {"message": "Employee not found."}, HTTPStatus.NOT_FOUND

        return jsonify({"data": dict(employee)})


class Quote(Resource):
    """Resource returning a simplified stock quote."""

    def get(self, ticker: str) -> Any:
        fetcher: QuoteFetcher = current_app.config["QUOTE_FETCHER"]
        symbol = ticker.upper()

        try:
            data = fetcher(symbol)
            previous_close = data["Previous Close"]
            target_estimate = data.get("1y Target Est")
        except KeyError:
            return {
                "message": "Quote data returned incomplete information.",
                "ticker": symbol,
            }, HTTPStatus.BAD_GATEWAY
        except Exception as exc:  # pragma: no cover - defensive
            current_app.logger.exception("Failed to fetch quote for %s", symbol)
            return {
                "message": "Unable to retrieve quote at this time.",
                "ticker": symbol,
                "details": str(exc),
            }, HTTPStatus.BAD_GATEWAY

        return jsonify(
            {
                "quote": [
                    {
                        "ticker": symbol,
                        "price": previous_close,
                        "target_estimate": target_estimate,
                    }
                ]
            }
        )


def create_app(database_url: str = "sqlite:///chinook.db", quote_fetcher: QuoteFetcher | None = None) -> Flask:
    """Application factory used by the tests and the CLI entry point."""

    app = Flask(__name__)
    api = Api(app)

    engine = create_engine(database_url, future=True)
    app.config["DB_ENGINE"] = engine
    app.config["QUOTE_FETCHER"] = quote_fetcher or default_quote_fetcher

    api.add_resource(Employees, "/employees")
    api.add_resource(Tracks, "/tracks")
    api.add_resource(Employee, "/employees/<int:employee_id>")
    api.add_resource(Quote, "/quote/<string:ticker>")

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Chinook API service")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind to")
    parser.add_argument("--port", type=int, default=5002, help="Port to listen on")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    parser.add_argument(
        "--database-url",
        default="sqlite:///chinook.db",
        help="SQLAlchemy connection string to the Chinook database",
    )
    args = parser.parse_args()

    app = create_app(args.database_url)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
