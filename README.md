
# NYT ETL Pipeline

This project implements an ETL pipeline to fetch and analyze articles from the New York Times API.

# Project Structure

```
NYT/
├── Choose_Month/
│   └── articles.py
├── Generate_Charts/
│   ├── bar_chart.py
│   └── generate_wordcloud.py
├── Last_Month/
│   ├── last_month_articles.py
│   ├── last_month_transform_headlines.py
│   └── run_etl_last_month.py
├── data/
│   ├── common_words_YYYY-MM-DD.csv
│   └── nyt_articles.db
├── logs/
│   └── data_fetch.log
├── plots/
│   ├── common_words_plot_YYYY-MM-DD.png
│   └── common_words_cloud_YYYY-MM-DD.png
├── analyze_headlines.py
├── drop_all_tables.py
└── README.md
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
python   run_etl_last_month.py
```

Soon will implement more options


