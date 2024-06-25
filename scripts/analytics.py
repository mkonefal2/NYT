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

# Application Title
st.title('Headline Analysis of the Last Month')

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation
st.sidebar.title('Navigation')
option = st.sidebar.selectbox('Select Page', ['Headline Analysis of the Last Month', 'Run ETL', 'Data', 'SQL Analysis'])

# Page for word cloud analysis
if option == 'Headline Analysis of the Last Month':
    st.header('Common Words Cloud')

    wordcloud_filename = get_previous_month_filename('common_words_cloud_%Y_%m.png')
    wordcloud_path = os.path.join('static/plots', wordcloud_filename)

    if os.path.exists(wordcloud_path):
        wordcloud_image = Image.open(wordcloud_path)
        st.image(wordcloud_image, caption='Word Cloud')
    else:
        st.error(f"Word Cloud file not found: {wordcloud_path}")

    # Generating common_words_plot
    table_name = get_previous_month_table_name()
    query = f"""
    SELECT word, count
    FROM "{table_name}"
    ORDER BY count DESC
    LIMIT 10;
    """
    data = execute_query(query)

    if not data.empty:
        st.subheader('Common Words Plot')
        
        col1 = st.columns(1)[0]  # Adjust width ratios
        
        with col1:
            # Data is already sorted by 'count' in descending order due to the SQL query
            st.bar_chart(data.set_index('word'))
    else:
        st.error("No data found for common words plot.")

    # Setting background color
    st.markdown('<style>body{background-color: #232136;}</style>', unsafe_allow_html=True)

# Page for running ETL
elif option == 'Run ETL':
    st.header('Run ETL')

    with st.form('run_etl_form'):
        year = st.text_input('Year')
        month = st.text_input('Month')
        submitted = st.form_submit_button('Run ETL')
        if submitted:
            script_path = os.path.join('scripts', 'word_count_headline_analysis', 'run_etl.py')
            result = subprocess.run(['python', script_path, year, month], capture_output=True, text=True)
            if result.returncode == 0:
                st.success('ETL script executed successfully')
            else:
                st.error(f"ETL script error: {result.stderr}")

# Page for displaying data from the database
elif option == 'Data':
    st.header('Data')

    db_path = os.path.join('data', 'nyt_articles.db')
    con = duckdb.connect(database=db_path)

    today = datetime.today()
    default_year = today.year
    default_month = today.month

    year = st.number_input('Year', min_value=2000, max_value=2100, value=default_year)
    month = st.number_input('Month', min_value=1, max_value=12, value=default_month)

    if st.button('Load Data'):
        try:
            query = f"""
                SELECT * FROM articles 
                WHERE strftime('%Y', pub_date) = '{year}' AND strftime('%m', pub_date) = '{month:02d}'
            """
            df = con.execute(query).df()
            if not df.empty:
                st.write(f"Query returned {len(df)} rows")
                st.dataframe(df)
            else:
                st.warning("No data found for the selected month.")
        except Exception as e:
            st.error(f"Error connecting to database: {e}")

# Page for SQL analysis
elif option == 'SQL Analysis':
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
    col1, col2, col3, col4, col5, col6 = st.columns(6)

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
    with col6:
        show_avg_word_count_by_source = st.button('Average Word Count by Source')

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

    # Button and results for "Average Word Count by Source"
    if show_avg_word_count_by_source:
        query = load_query('sql/avg_word_count_by_source.sql')
        data = execute_query(query)
        col1, col2 = st.columns([1, 3])  # Adjust width ratios
        
        with col1:
            st.write(data)

        with col2:
            st.bar_chart(data.set_index('source'))