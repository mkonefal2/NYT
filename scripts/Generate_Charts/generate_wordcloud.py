import pandas as pd
from wordcloud import WordCloud
import os
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

class WordCloudGenerator:
    def __init__(self, csv_dir, output_dir):
        previous_month_date = datetime.datetime.now() - relativedelta(months=1)
        self.current_date = previous_month_date.strftime("%Y-%m")
        self.csv_path = os.path.join(csv_dir, f"common_words_{self.current_date}.csv")
        self.output_dir = output_dir

    def load_data(self):
        return pd.read_csv(self.csv_path)

    def generate_wordcloud(self, data):
        words_dict = data.set_index('word')['count'].to_dict()
        wordcloud = WordCloud(width=1152, height=648, background_color='#232136').generate_from_frequencies(words_dict)

        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        plot_path = os.path.join(self.output_dir, f"common_words_cloud_{self.current_date}.png")
        wordcloud.to_file(plot_path)
        print(f"Word cloud saved to {plot_path}")

    def run(self):
        data = self.load_data()
        self.generate_wordcloud(data)

if __name__ == '__main__':
    csv_dir = r"C:\Projekty\NYT\data"
    output_dir = os.path.join(os.path.dirname(__file__), '../plots')

    generator = WordCloudGenerator(csv_dir, output_dir)
    generator.run()