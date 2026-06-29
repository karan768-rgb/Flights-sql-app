# Flights Analysis

A Streamlit dashboard for exploring Indian domestic flight data — search flights between cities and view overall trends (busiest airports, airline market share, pricing, durations) from a MySQL-backed dataset.

## Screenshots

**Home**
![Home page](<img width="1918" height="1012" alt="Screenshot 2026-06-29 224611" src="https://github.com/user-attachments/assets/fd092219-caa4-4c86-90f0-ae29e4c2bba3" />
)

**Check Flights**
![Check flights page](<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/7fc9013c-fad6-4133-aa38-527229592326" />
)

**Analytics**
![Analytics charts continued](<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/d514f4ea-31e3-425d-9565-c9143f7d1b5f" />
)
![Analytics overview](<img width="1917" height="1012" alt="image" src="https://github.com/user-attachments/assets/9a6f8ea2-192e-4873-bd1d-bc9c83c4617e" />
)
![Analytics charts](<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/d6386de5-fa91-4229-b963-6af487a672ac" />
)


> Live demo isn't available since the app connects to a local MySQL instance. Run it locally using the steps below.

## Features

- **Check Flights** — pick a source and destination city and see matching flights: airline, route, departure time, duration, and price.
- **Analytics**
  - Total flights, average/min/max price
  - Airline frequency (pie chart)
  - Busiest airports (bar chart)
  - Daily flight frequency (line chart)
  - Average price by airline
  - Distribution of non-stop / 1-stop / 2-stop flights
  - Average duration by number of stops
  - Top 10 most expensive routes

## Tech Stack

- **Python**, **Streamlit** — UI
- **MySQL** — data storage
- **pandas**, **SQLAlchemy** — CSV import into MySQL
- **Plotly** — charts
- **python-dotenv** — keeps DB credentials out of source code

## Project Structure

```
Flights-sql-app/
├── app.py              # Streamlit app (UI + page routing)
├── dbhelper.py          # DB class — all SQL queries live here
├── import_csv.py        # one-off script to load the CSV into MySQL
├── .env.example          # template for required environment variables
├── .gitignore
└── requirements.txt
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/karan768-rgb/flights-sql-app.git
cd flights-sql-app
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Set up MySQL

Create a database (name of your choice, e.g. `flights`):

```sql
CREATE DATABASE IF NOT EXISTS flights;
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your own MySQL credentials:

```
DB_HOST=127.0.0.1
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

### 5. Import the dataset

Update the CSV path in `import_csv.py`, then run it once to load the data into MySQL:

```bash
python import_csv.py
```

### 6. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Dataset

Indian domestic flights dataset with columns: `Airline, Date_of_Journey, Source, Destination, Route, Dep_Time, Duration, Total_Stops, Price`.

## Notes

- Not every source–destination pair has a direct flight in the dataset — searching an unavailable route will show a "no flights found" message rather than an empty table.
- Credentials are loaded from environment variables via `python-dotenv` and are never committed to the repo (`.env` is git-ignored; only `.env.example` is tracked).
