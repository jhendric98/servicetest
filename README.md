# Flask RESTful API for Chinook Database

This repository contains a Python script that demonstrates a Flask-based RESTful API for the Chinook database. The API provides endpoints to interact with the employees, tracks, and stock quotes. It uses Flask, Flask-RESTful, SQLAlchemy, and the yahoo_fin library.

## Requirements

Python 3.6 or higher is required to run this script. Before running the script, you need to install the required packages from the `requirements.txt` file. You can do this by running the following command:


## Overview

The API has four main endpoints:

1. `/employees`: To get a list of all employees and add a new employee.
2. `/tracks`: To get a list of tracks with their track ID, name, composer, and unit price.
3. `/employees/<employee_id>`: To get information about a specific employee by their employee ID.
4. `/quote/<ticker>`: To get a stock quote using the yahoo_fin library for a specific stock ticker.

## Instructions for Use

1. Clone this repository or download the script file.
2. Install the required packages using the command provided in the Requirements section.
3. Run the script with the following command:


4. Once the script is running, you can access the API by navigating to `http://localhost:5002` in your browser or by using API testing tools like Postman or curl.

Here are some sample requests for each endpoint:

- Get a list of all employees:
  - Method: `GET`
  - URL: `http://localhost:5002/employees`

- Add a new employee:
  - Method: `POST`
  - URL: `http://localhost:5002/employees`
  - Headers: `Content-Type: application/json`
  - Body: JSON object containing employee data (e.g., `{"LastName": "Doe", "FirstName": "John", "Title": "Sales Manager", ...}`)

- Get a list of tracks:
  - Method: `GET`
  - URL: `http://localhost:5002/tracks`

- Get information about an employee by their employee ID:
  - Method: `GET`
  - URL: `http://localhost:5002/employees/1`

- Get a stock quote for a specific stock ticker:
  - Method: `GET`
  - URL: `http://localhost:5002/quote/AAPL`

## Running Tests

The script includes a set of tests for the API endpoints. To run the tests, execute the script with the following command:


The tests will run before the Flask application starts, and the results will be displayed in the terminal.
