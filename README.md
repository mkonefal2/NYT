
# NYT ETL Pipeline

This project implements an ETL pipeline to fetch and analyze articles from the New York Times API.

# Project Structure

```
NYT/
│
├── app/
│   ├── __pycache__/
│   ├── templates/
│   │   ├── base.html
│   │   ├── data.html
│   │   ├── etl.html
│   │   ├── index.html
│   ├── __init__.py
│   ├── routes.py
│
├── data/
│   ├── common_words_2023-12.csv
│   ├── common_words_2024-05.csv
│   ├── lastm_headline_analysis_2024-05.csv
│   ├── nyt_articles.db
│
├── logs/
│   ├── data_fetch.log
│
├── notebooks/
│   ├── view_all_articles.ipynb
│
├── scripts/
│   ├── __pycache__/
│   ├── word_count_headline_analysis/
│   │   ├── analyze_headlines.py
│   ├── articles.py
│   ├── bar_chart.py
│   ├── generate_wordcloud.py
│   ├── run_etl.py
│   ├── transform_headlines.py
│   ├── drop_all_tables.py
│
├── sql/
│
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   ├── test.css
│   ├── plots/
│       ├── common_words_cloud_YYYY_M.png
│       ├── common_words_plot_YYYY_M.png
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── run.py

```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` package installer

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mkonefal2/NYT.git
cd NYT
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

To run the ETL pipeline for last month, execute the following script:

```bash
python  ./scripts/word_count_headline_analysis/run_etl.py
```

Output will be visible in :
```bash
./static/plots/
```

You can also run web app 
```
python ./scripts/run.py
```
