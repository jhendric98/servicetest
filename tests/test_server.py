import os
import sqlite3
import tempfile
import unittest
from unittest.mock import Mock

from chinook_service.server import create_app

EMPLOYEES_SCHEMA = """
CREATE TABLE employees (
    EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT,
    LastName NVARCHAR(20) NOT NULL,
    FirstName NVARCHAR(20) NOT NULL,
    Title NVARCHAR(30),
    ReportsTo INTEGER,
    BirthDate DATETIME,
    HireDate DATETIME,
    Address NVARCHAR(70),
    City NVARCHAR(40),
    State NVARCHAR(40),
    Country NVARCHAR(40),
    PostalCode NVARCHAR(10),
    Phone NVARCHAR(24),
    Fax NVARCHAR(24),
    Email NVARCHAR(60)
);
"""

TRACKS_SCHEMA = """
CREATE TABLE tracks (
    TrackId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name NVARCHAR(200) NOT NULL,
    Composer NVARCHAR(220),
    UnitPrice NUMERIC(10, 2) NOT NULL
);
"""


class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        conn = sqlite3.connect(self.db_path)
        conn.executescript(EMPLOYEES_SCHEMA)
        conn.executescript(TRACKS_SCHEMA)
        conn.execute(
            "INSERT INTO employees "
            "(LastName, FirstName, Title, Address, City, Country, Phone, Email) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Doe",
                "Jane",
                "Manager",
                "123 Main",
                "Springfield",
                "USA",
                "555-1234",
                "jane@example.com",
            ),
        )
        conn.execute(
            "INSERT INTO tracks (Name, Composer, UnitPrice) VALUES (?, ?, ?)",
            ("Foobar", "Composer", 0.99),
        )
        conn.commit()
        conn.close()

        self.quote_fetcher = Mock(return_value={"Previous Close": 100.0, "1y Target Est": 120.0})
        app = create_app(f"sqlite:///{self.db_path}", quote_fetcher=self.quote_fetcher)
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self) -> None:
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_employees_list(self) -> None:
        response = self.client.get("/employees")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("employees", payload)
        self.assertEqual(len(payload["employees"]), 1)

    def test_employees_create(self) -> None:
        body: dict[str, str] = {
            "LastName": "Smith",
            "FirstName": "John",
            "Title": "Sales Rep",
            "Address": "456 Second",
            "City": "Springfield",
            "Country": "USA",
            "Phone": "555-6789",
            "Email": "john@example.com",
        }
        response = self.client.post("/employees", json=body)
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["LastName"], body["LastName"])

    def test_employees_create_rejects_missing_fields(self) -> None:
        response = self.client.post("/employees", json={"FirstName": "Only"})
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertIn("fields", payload)

    def test_employee_lookup_not_found(self) -> None:
        response = self.client.get("/employees/9999")
        self.assertEqual(response.status_code, 404)

    def test_tracks(self) -> None:
        response = self.client.get("/tracks")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["data"][0]["Name"], "Foobar")

    def test_quote(self) -> None:
        response = self.client.get("/quote/AAPL")
        self.assertEqual(response.status_code, 200)
        self.quote_fetcher.assert_called_once_with("AAPL")
        payload = response.get_json()
        self.assertEqual(payload["quote"][0]["price"], 100.0)

    def test_quote_handles_key_error(self) -> None:
        self.quote_fetcher.side_effect = KeyError("Previous Close")
        response = self.client.get("/quote/MSFT")
        self.assertEqual(response.status_code, 502)
        payload = response.get_json()
        self.assertIn("message", payload)


if __name__ == "__main__":
    unittest.main()
