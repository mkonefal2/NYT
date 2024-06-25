from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
import duckdb
import logging
from datetime import datetime, timedelta

main = Blueprint('main', __name__, static_folder='../static', static_url_path='/static')

def get_previous_month_filename(filename_template):
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime(filename_template)

@main.route('/')
def index():
    wordcloud_filename = get_previous_month_filename('plots/common_words_cloud_%Y_%m.html')
    linechart_filename = get_previous_month_filename('plots/common_words_plot_%Y_%m.html')

    logging.info(f"Word Cloud file: {wordcloud_filename}")
    logging.info(f"Line Chart file: {linechart_filename}")

    wordcloud_path = os.path.join(main.static_folder, wordcloud_filename)
    linechart_path = os.path.join(main.static_folder, linechart_filename)

    if os.path.exists(wordcloud_path) and os.path.exists(linechart_path):
        logging.info("Both files exist.")
    else:
        if not os.path.exists(wordcloud_path):
            logging.error(f"Word Cloud file not found: {wordcloud_path}")
        if not os.path.exists(linechart_path):
            logging.error(f"Line Chart file not found: {linechart_path}")
    
    return render_template('index.html', wordcloud_filename=wordcloud_filename, linechart_filename=linechart_filename)

@main.route('/run_etl', methods=['GET', 'POST'])
def run_etl():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        script_path = os.path.join(os.path.dirname(__file__), '../scripts/word_count_headline_analysis/run_etl.py')
        subprocess.run(['python', script_path, year, month])
        return redirect(url_for('main.data'))
    return render_template('etl.html')

@main.route('/data', methods=['GET', 'POST'])
def data():
    db_path = os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db')
    logging.info(f"Database path: {db_path}")
    
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
    else:
        today = datetime.today()
        year = today.year
        month = today.month
    
    try:
        con = duckdb.connect(database=db_path)
        query = f"""
            SELECT * FROM articles 
            WHERE strftime('%Y', pub_date) = '{year}' AND strftime('%m', pub_date) = '{month:02d}'
        """
        df = con.execute(query).df()
        logging.info(f"Query returned {len(df)} rows")
        if not df.empty:
            logging.debug(f"Dataframe:\n{df.head()}")
            table_html = df.to_html(classes='data table table-striped', index=False)
        else:
            table_html = None
        return render_template('data.html', tables=[table_html] if table_html else [], titles=df.columns.values, selected_year=year, selected_month=month, datetime=datetime)
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return f"An error occurred: {e}", 500

@main.route('/static/<path:filename>')
def static_files(filename):
    logging.info(f"Serving static file: {filename}")
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../static'), filename)
