import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import datetime

# Wczytaj DataFrame z pliku CSV
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
csv_path = os.path.join(os.path.dirname(__file__), f"C:\\Projekty\\NYT\\data\\common_words_{current_date}.csv")
common_words_df = pd.read_csv(csv_path)

# Przygotuj dane do chmury słów (konwersja DataFrame na słownik)
words_dict = common_words_df.set_index('word')['count'].to_dict()

# Utwórz obiekt WordCloud
wordcloud = WordCloud(width=1152, height=648, background_color='#232136').generate_from_frequencies(words_dict)

# Wyświetl chmurę słów
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Usuń osie

# Zapisz chmurę słów do pliku PNG w katalogu `plots`
plots_dir = os.path.join(os.path.dirname(__file__), "../plots")
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
plot_path = os.path.join(plots_dir, f"common_words_cloud_{current_date}.png")
wordcloud.to_file(plot_path)

print(f"Word cloud saved to {plot_path}")