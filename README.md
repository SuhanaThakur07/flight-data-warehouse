# ✈️ Flight Data Warehouse

A Data Warehouse project built with Django and PostgreSQL featuring OLAP queries on real flight data.

## Dataset
- Source: Kaggle - US Flight Delays 2015
- 100,000 flight records shrink to 10000 rows .

## Tech Stack
- Python / Django
- PostgreSQL
- pgAdmin

## Star Schema
- FactFlights (Fact Table)
- DimAirline, DimAirport, DimDate, DimCancellation (Dimensions)

## OLAP Operations
- ROLLUP
- CUBE
- SLICE
- DICE
- DRILL DOWN

## How to Run
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Run server: `python manage.py runserver`