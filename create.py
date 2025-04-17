import os

BASE_DIR = "/mnt/d/Projekty/NYT-main"

# Struktura katalogów
folders = [
    f"{BASE_DIR}/scripts",
    f"{BASE_DIR}/airflow/dags",
    f"{BASE_DIR}/data",
    f"{BASE_DIR}/logs"
]

# Pliki i ich zawartość
files = {
    f"{BASE_DIR}/scripts/fetch_articles.py": "<ZAWARTOŚĆ FETCH_ARTICLES.PY>",
    f"{BASE_DIR}/scripts/transform_headlines.py": "<ZAWARTOŚĆ TRANSFORM_HEADLINES.PY>",
    f"{BASE_DIR}/scripts/analyze_keywords.py": "<ZAWARTOŚĆ ANALYZE_KEYWORDS.PY>",
    f"{BASE_DIR}/airflow/dags/nyt_articles_pipeline.py": "<ZAWARTOŚĆ DAG-A>",
    f"{BASE_DIR}/.env": "# NYT_API_KEY=your_api_key_here\n",
    f"{BASE_DIR}/data/.gitkeep": "",
    f"{BASE_DIR}/logs/.gitkeep": ""
}

# Tworzenie katalogów
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Tworzenie plików z zawartością
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Struktura projektu została utworzona w: {BASE_DIR}")
