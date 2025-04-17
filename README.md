Oczywiście! Oto angielska wersja pliku `README.md`:

---

```markdown
# 📰 NYT Headlines Pipeline with Airflow

A data pipeline for analyzing New York Times article headlines using Apache Airflow, DuckDB, and the NYT Archive API.

---

## 🧩 Features

The pipeline consists of three steps:

1. **fetch_articles.py**  
   ➤ Downloads articles from the NYT API for a given month and stores them in a DuckDB database.

2. **transform_headlines.py**  
   ➤ Filters and extracts headlines from that month into a dedicated table and CSV file.

3. **analyze_keywords.py**  
   ➤ Analyzes the most frequent words in the headlines and saves the results to DuckDB and a CSV.

---

## 🗂 Project Structure

```
nyt_airflow_project/
├── airflow/
│   └── dags/
│       └── nyt_articles_pipeline.py
├── scripts/
│   ├── fetch_articles.py
│   ├── transform_headlines.py
│   └── analyze_keywords.py
├── data/                 ← output CSV files + DuckDB database
├── logs/                 ← ETL logs
├── .env                  ← NYT API key
└── requirements.txt
```

---

## 🔐 Environment File

Create a `.env` file in the project root and add your NYT API key:

```dotenv
NYT_API_KEY=your_nyt_api_key_here
```

---

## 🚀 Local Execution (for testing)

```bash
# (Optional) Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test one step manually
python scripts/fetch_articles.py
```

---

## 🗓 Airflow DAG Configuration

The `nyt_articles_pipeline` DAG runs daily and processes data from the **previous month** relative to the execution date.

Once Airflow is running, view the DAG at:

```bash
airflow webserver
airflow scheduler
```

---

## 📊 Output Data

Generated CSV files and DuckDB tables can be found in the `data/` folder, e.g.:

- `headline_analysis_2024-03.csv`
- `common_words_2024-03.csv`
- DuckDB tables: `articles`, `headline_analysis_YYYY_MM`, `common_words_YYYY_MM`

---

## 🛠 Requirements

Recommended setup (see `requirements.txt`):

- Python 3.9+
- Apache Airflow 2.8+
- DuckDB
- requests, pandas, dotenv

---

## 📄 License

This project is intended for educational and personal use. Licensed under the MIT License.
```

---

Gotowy na `.gitignore`?