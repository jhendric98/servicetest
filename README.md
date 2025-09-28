# Flask RESTful API for the Chinook Database

This project exposes a small portion of the [Chinook sample database](https://github.com/lerocha/chinook-database) through a Flask RESTful API.  It demonstrates safe data access patterns, lightweight request validation, and graceful integration with the [`yahoo_fin`](https://theautomatic.net/yahoo_fin-documentation/) library for retrieving stock quotes.

## Features

* Employees endpoint that supports listing and creating employee records with basic validation.
* Tracks endpoint that surfaces readonly track metadata.
* Quote endpoint that sanitises the requested ticker symbol and degrades gracefully when Yahoo Finance cannot provide data.
* Configurable database connection string and quote fetcher for testing or local development.

## Getting Started

### Prerequisites

* Python 3.9 or later (the code relies on modern typing features and SQLAlchemy 2 behaviour).
* A SQLite copy of the Chinook database (one is shipped as `chinook.db`).

### Installation

You can install the dependencies with either the built-in `venv` module or with
the [uv](https://github.com/astral-sh/uv) package manager.  The uv workflow is
recommended because it understands the `pyproject.toml` included in this
repository and can resolve optional dependency groups in a single command.

#### Using uv (recommended)

1. Create the environment (this uses the Python from your `$PATH`):

   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. Install the application and development dependencies defined in
   `pyproject.toml`:

   ```bash
   uv sync --all-groups
   ```

   The `--all-groups` flag installs the default runtime dependencies as well as
   the optional development tools listed under `[tool.uv]` in
   `pyproject.toml`.

#### Using pip

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies from `requirements.txt`:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

### Running the API

Start the service with:

```bash
python server.py --database-url sqlite:///chinook.db --host 0.0.0.0 --port 5002
```

The command line options are optional; they allow you to point to an alternative database, bind to a specific interface, or change the port.  Once running, the API will be available at `http://localhost:5002`.

### Example Requests

```bash
# List all employees
curl http://localhost:5002/employees

# Create an employee
curl -X POST http://localhost:5002/employees \
     -H "Content-Type: application/json" \
     -d '{
           "LastName": "Doe",
           "FirstName": "Janet",
           "Title": "Sales Manager",
           "Address": "123 Main",
           "City": "Springfield",
           "Country": "USA",
           "Phone": "555-1234",
           "Email": "janet.doe@example.com"
         }'

# Fetch a single employee
curl http://localhost:5002/employees/1

# List tracks
curl http://localhost:5002/tracks

# Fetch a quote (depends on Yahoo Finance availability)
curl http://localhost:5002/quote/AAPL
```

### Running Tests

The automated test-suite spins up a temporary database and stubs the Yahoo Finance integration.  Execute it with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Security Considerations

* SQL queries rely on SQLAlchemy parameter binding to avoid injection vulnerabilities.
* All employee payloads are validated for missing or unexpected fields before hitting the database.
* External quote lookups are wrapped with error handling so the API does not crash when the data source is unavailable.

For details on supported versions and how to report security issues, see [SECURITY.md](SECURITY.md).
