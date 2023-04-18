#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text
from json import dumps
from yahoo_fin import stock_info
import unittest

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)


class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute(text("SELECT * FROM employees"))  # This line performs query and returns json result
        result = [dict(row) for row in query.fetchall()]
        return {'employees': result}

    def post(self):
        conn = db_connect.connect()
        employee_data = request.get_json()
        query = text("""INSERT INTO employees (LastName, FirstName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Country, PostalCode, Phone, Fax, Email)
                        VALUES (:LastName, :FirstName, :Title, :ReportsTo, :BirthDate, :HireDate, :Address, :City, :State, :Country, :PostalCode, :Phone, :Fax, :Email)""")
        conn.execute(query, **employee_data)
        return {'status': 'success'}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(text("SELECT trackid, name, composer, unitprice FROM tracks;"))
        result = [dict(row) for row in query.fetchall()]
        return jsonify({'data': result})


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute(text("SELECT * FROM employees WHERE EmployeeId = :employee_id"), employee_id=int(employee_id))
        result = [dict(row) for row in query.fetchall()]
        return jsonify({'data': result})


class Quote(Resource):
    def get(self, ticker):
        quote = stock_info.get_quote_table(ticker.upper())
        result = {'quote': [{'ticker': ticker.upper(), 'price': quote['Previous Close'], 'trade_dt': quote['1y Target Est']}]}
        return jsonify(result)


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3
api.add_resource(Quote, '/quote/<ticker>')  # new route


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_employees(self):
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)

    def test_tracks(self):
        response = self.app.get('/tracks')
        self.assertEqual(response.status_code, 200)

    def test_employee_name(self):
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, 200)

    def test_quote(self):
        response = self.app.get('/quote/AAPL')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    app.run(host='0.0.0.0', port='5002')
