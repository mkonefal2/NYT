import subprocess

# List of scripts to run
scripts = [
    "scripts/last_month_articles.py",
    "scripts/transform_headlines.py",
    "scripts/analyze_headlines.py",
    "scripts/bar_chart.py"
]

all_success = True

for script in scripts:
    result = subprocess.run(["python", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}")
        print(result.stderr)
        all_success = False
        break
    else:
        print(f"Successfully ran {script}")
        print(result.stdout)

if all_success:
    print("ETL process completed successfully.")
else:
    print("ETL process encountered an error.")
