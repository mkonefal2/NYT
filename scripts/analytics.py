import streamlit as st
import duckdb
import pandas as pd
import os
import subprocess
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt

# Function Definitions
def load_query(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_previous_month_date_range():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    start_date = last_month.replace(day=1)
    end_date = last_month
    return start_date, end_date

def get_previous_month_table_name():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime('common_words_%Y-%m')

def get_previous_month_filename(filename_template):
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime(filename_template)

def load_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to execute SQL query
def execute_query(query):
    conn = duckdb.connect(database='data/nyt_articles.db')
    result = conn.execute(query).df()
    conn.close()
    return result

def data_exists(year, month):
    query = f"""
        SELECT COUNT(*) AS count
        FROM articles
        WHERE strftime('%Y', pub_date) = '{year}' AND strftime('%m', pub_date) = '{month:02d}'
    """
    result = execute_query(query)
    return result['count'][0] > 0

def log_etl_output(output, error):
    log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, 'etl_log.txt')
    with open(log_filename, 'a') as log_file:
        log_file.write(f"{datetime.now()}\n")
        log_file.write("Output:\n")
        log_file.write(output)
        log_file.write("\nError:\n")
        log_file.write(error)
        log_file.write("\n" + "-"*50 + "\n")

# Application Title
st.title('Headline Analysis and ETL')

# Inject CSS to style the page
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding: 1rem;
    }
    .stButton > button {
        width: 100%;
    }
    .css-18e3th9 {
        padding-top: 4rem;
    }
    h1 {
        margin-top: 2rem;
    }
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
# Sidebar for Load Data panel
st.sidebar.title('Load Data')
db_path = os.path.join('data', 'nyt_articles.db')
today = datetime.today()
default_year = today.year
default_month = today.month

years = list(range(2000, today.year + 1))
months = list(range(1, 13))

col1, col2 = st.sidebar.columns(2)
with col1:
    year = st.selectbox('Year', years, index=years.index(default_year))
with col2:
    month = st.selectbox('Month', months, index=months.index(default_month))

if st.sidebar.button('Run ETL'):
    # Check if data already exists for the selected month
    if data_exists(year, month):
        st.sidebar.info('Data already exists for the selected month.')
    else:
        # Close any existing connections before running ETL script
        try:
            duckdb_conn = duckdb.connect(database=db_path)
            duckdb_conn.close()
        except Exception as e:
            st.sidebar.error(f"Error closing existing database connection: {e}")

        # Run ETL script
        script_path = os.path.join('scripts', 'word_count_headline_analysis', 'run_etl.py')
        result = subprocess.run(['python', script_path, str(year), str(month)], capture_output=True, text=True)
        log_etl_output(result.stdout, result.stderr)
        if result.returncode == 0:
            st.sidebar.success('ETL script executed successfully')
        else:
            st.sidebar.error('ETL script execution failed')

if st.sidebar.button('Drop Data'):
    # Drop data for the selected month
    try:
        query = f"""
            DELETE FROM articles 
            WHERE strftime('%Y', pub_date) = '{year}' AND strftime('%m', pub_date) = '{month:02d}'
        """
        duckdb_conn = duckdb.connect(database=db_path)
        duckdb_conn.execute(query)
        duckdb_conn.close()
        st.sidebar.success(f"Data for {year}-{month:02d} dropped successfully.")
    except Exception as e:
        st.sidebar.error(f"Error dropping data: {e}")





# Page for word cloud analysis and SQL analysis
st.header('Last Month Words Analysis')

wordcloud_filename = get_previous_month_filename('common_words_cloud_%Y_%m.png')
wordcloud_path = os.path.join('static/plots', wordcloud_filename)
wordplot_filename = get_previous_month_filename('common_words_plot_%Y_%m.html')
wordplot_path = os.path.join('static/plots', wordplot_filename)

col1, col2 = st.columns(2)  # Create two columns
with col1:  # Use first column to display the image
    if os.path.exists(wordcloud_path):
        wordcloud_image = Image.open(wordcloud_path)
        st.image(wordcloud_image)
    else:
        st.error(f"Word Cloud file not found: {wordcloud_path}")

with col2:  # Use second column to display the plot
    if os.path.exists(wordplot_path):
        with open(wordplot_path, 'r', encoding='utf-8') as file:
            wordplot_html = file.read()
        # Add CSS to scale the HTML content
        scaled_html = f"""
        <div style="transform: scale(0.8); transform-origin: top left;">
            {wordplot_html}
        </div>
        """
        
        st.components.v1.html(scaled_html, height=400, width=850)
    else:
        st.error(f"Common Words Plot file not found: {wordplot_path}")

st.header('SQL Analysis')

# Inject CSS to expand the layout width for SQL Analysis
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding: 1rem;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout for buttons
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

with col1:
    show_articles_per_month = st.button('Number of Articles per Month')
with col2:
    show_articles_by_type = st.button('Articles by Type')
with col3:
    show_top_headlines = st.button('Top Headlines by Word Count')
with col4:
    show_articles_by_news_desk = st.button('Articles by News Desk')
with col5:
    show_articles_by_word_count_range = st.button('Articles by Word Count Range')

st.write("")

# Button and results for "Articles per Month"
if show_articles_per_month:
    query = load_query('sql/articles_per_month.sql')
    data = execute_query(query)
    col1, col2 = st.columns([1, 3])  # Adjust width ratios
    
    with col1:
        st.write(data)

    with col2:
        st.line_chart(data.set_index('month'))

# Button and results for "Articles by Type"
if show_articles_by_type:
    query = load_query('sql/articles_by_type.sql')
    data = execute_query(query)
    col1, col2 = st.columns([1, 3])  # Adjust width ratios
    
    with col1:
        st.write(data)

    with col2:
        st.bar_chart(data.set_index('type_of_material'))

# Button and results for "Top Headlines"
if show_top_headlines:
    query = load_query('sql/top_headlines.sql')
    data = execute_query(query)
    col1 = st.columns(1)[0]  # Access the first column directly
    
    with col1:
        st.write(data)

# Button and results for "Articles by News Desk"
if show_articles_by_news_desk:
    query = load_query('sql/articles_by_news_desk.sql')
    data = execute_query(query)
    col1, col2 = st.columns([1, 3])  # Adjust width ratios
    
    with col1:
        st.write(data)

    with col2:
        st.bar_chart(data.set_index('news_desk'))

# Button and results for "Articles by Word Count Range"
if show_articles_by_word_count_range:
    query = load_query('sql/articles_by_word_count_range.sql')
    data = execute_query(query)
    col1, col2 = st.columns([1, 3])  # Adjust width ratios
    
    with col1:
        st.write(data)

    with col2:
        st.bar_chart(data.set_index('word_count_range'))

# Load data from database and display at the bottom
st.header('Data Table')

if st.sidebar.button('Load Data'):
    # Load data from database
    try:
        query = f"""
            SELECT * FROM articles 
            WHERE strftime('%Y', pub_date) = '{year}' AND strftime('%m', pub_date) = '{month:02d}'
        """
        duckdb_conn = duckdb.connect(database=db_path)
        df = duckdb_conn.execute(query).df()
        duckdb_conn.close()
        if not df.empty:
            st.write(f"Query returned {len(df)} rows")
            st.dataframe(df)
        else:
            st.warning("No data found for the selected month.")
    except Exception as e:
        st.error(f"Error connecting to database: {e}")

# Setting background color
st.markdown('<style>body{background-color: #232136;}</style>', unsafe_allow_html=True)
