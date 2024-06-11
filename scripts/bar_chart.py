import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime

# Załaduj DataFrame z pliku CSV
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
csv_path = os.path.join(os.path.dirname(__file__), f"../data/common_words_{current_date}.csv")
common_words_df = pd.read_csv(csv_path)
# Filtracja do 10 najczęściej występujących słów
common_words_df = common_words_df.nlargest(10, 'count')
# Generowanie wykresu z ciemniejszym tłem
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#232136')  # Ustawienie koloru tła dla całej figury
ax.set_facecolor('#232136')  # Ustawienie koloru tła dla obszaru wykresu

plt.bar(common_words_df['word'], common_words_df['count'], color='#ec9b99')
plt.xlabel('Words', color='white')
plt.ylabel('Count', color='white')
plt.xticks(rotation=45, color='white')
plt.yticks(color='white')
plt.title('Most Common Words in NYT Headlines', color='white')
plt.tight_layout()

# Zapisz wykres do pliku PNG w katalogu `plots`
plots_dir = os.path.join(os.path.dirname(__file__), f"../plots")
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
plot_path = os.path.join(plots_dir, f"common_words_plot_{current_date}.png")

# Zapisz wykres do pliku PNG z ciemnym tłem
plt.savefig(plot_path, facecolor=fig.get_facecolor())

plt.savefig(plot_path)

print(f"Plot saved to {plot_path}")