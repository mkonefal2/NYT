import subprocess
import os
import argparse
import datetime
import time

def run_script(script, year, month):
    result = subprocess.run(["python", script, str(year), str(month)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}")
        print(result.stderr)
        return False
    else:
        print(f"Successfully ran {script}")
        print(result.stdout)
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run ETL process for a selected month.')

    # Calculate the previous month and year
    current_date = datetime.datetime.now()
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
    previous_year = last_day_of_previous_month.year
    previous_month = last_day_of_previous_month.month

    # Set default values for the year and month arguments
    parser.add_argument('year', type=int, help='Year of the articles to fetch', default=previous_year, nargs='?')
    parser.add_argument('month', type=int, help='Month of the articles to fetch', default=previous_month, nargs='?')
    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    scripts = [
        os.path.join(current_dir, "articles.py"),
        os.path.join(current_dir, "transform_headlines.py"),
        os.path.join(current_dir, "analyze_headlines.py"),
        os.path.join(current_dir, "bar_chart.py"),
        os.path.join(current_dir, "bar_chart_html.py"),
        os.path.join(current_dir, "generate_wordcloud_html.py"),
        os.path.join(current_dir, "generate_wordcloud.py")
    ]

    all_success = True

    for script in scripts:
        success = run_script(script, args.year, args.month)
        if not success:
            all_success = False
            break
        time.sleep(5)  # Opóźnienie 15 sekund przed uruchomieniem następnego skryptu
    if all_success:
        print("ETL process completed successfully.")
    else:
        print("ETL process encountered an error.")
