
# NYT ETL Pipeline

This project implements an ETL pipeline to fetch and analyze articles from the New York Times API.

# Project Structure

```
NYT/
├── .github/
│   └── workflows/
│   └── ci.yml
├── data/
│   ├── common_words_YYYY-MM-DD.csv
│   ├── headline_analysis_YYYY-MM-DD.csv
│   ├── nyt_articles.db
├── logs/
│   └── data_fetch.log
├── notebooks/
├── plots/
│   └── common_words_plot_YYYY-MM-DD.png
├── scripts/
│   ├── analyze_headlines.py
│   ├── bar_chart.py
│   ├── drop_all_tables.py
│   ├── last_month_articles.py
│   ├── run_etl.py
│   └── transform_headlines.py
├── sql/
├── tests/
│   └── test_etl_scripts.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── ci.yml
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` package installer

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mkonefal2/NYT-Live.git
cd NYT-Live
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API key:

```plaintext
NYT_API_KEY=your_actual_api_key_here
```

## Usage

To run the ETL pipeline, execute the following scripts in order:

```bash
python scripts/last_month_articles.py
python scripts/transform_headlines.py
python scripts/analyze_headlines.py
python scripts/bar_chart.py
```

