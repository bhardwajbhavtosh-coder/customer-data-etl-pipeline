# Customer Data ETL Pipeline

## Project Overview
This project implements a simple ETL (Extract, Transform, Load) pipeline using Python and PostgreSQL. It reads customer data from a CSV file, cleans the data, and loads the processed records into a PostgreSQL database.

## ETL Workflow

### 1. Extract
- Read customer data from a CSV file using Pandas.
- Load the data into a DataFrame.

### 2. Transform
- Remove duplicate records.
- Handle missing values.
- Clean whitespace from text columns.
- Convert customer IDs and ages to numeric values.
- Filter invalid records.

### 3. Load
- Connect to PostgreSQL using SQLAlchemy.
- Load the cleaned data into the `customers` table.
- Verify the number of records loaded.

## Technologies Used
- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- psycopg2
- VS Code

## Project Structure

```text
data-engineering-project/
├── data/
│   └── customers.csv
├── src/
│   └── etl_pipeline.py
├── README.md
└── .gitignore
```

## How to Run

1. Install Python and PostgreSQL.
2. Install the required Python packages:

   ```bash
   pip install pandas sqlalchemy psycopg2-binary
   ```

3. Configure the PostgreSQL connection in `src/etl_pipeline.py`.
4. Place the input file at `data/customers.csv`.
5. Run the pipeline from the project root:

   ```bash
   python src/etl_pipeline.py
   ```

## Learning Outcomes
- Understanding the ETL process.
- Cleaning data with Pandas.
- Connecting Python to PostgreSQL.
- Loading structured data into a relational database.

## Future Improvements
- Store database credentials securely using environment variables.
- Add logging and error handling.
- Automate pipeline execution.
- Add data-quality checks.

**Status:** Beginner ETL project completed successfully.
