import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

from datetime import datetime
from dateutil.relativedelta import relativedelta

class BarChartGenerator:
    def __init__(self, csv_dir, output_dir):
        one_month_ago = datetime.now() - relativedelta(months=1)
        self.current_date = one_month_ago.strftime("%Y-%m")  # Format daty zawierający rok i miesiąc
        self.csv_path = os.path.join(csv_dir, f"common_words_{self.current_date}.csv")
        self.output_dir = output_dir

    def load_data(self):
        return pd.read_csv(self.csv_path)

    def generate_chart(self, data):
        data = data.nlargest(10, 'count')
        fig, ax = plt.subplots(figsize=(11.52, 6.48))
        fig.patch.set_facecolor('#232136')
        ax.set_facecolor('#232136')

        plt.bar(data['word'], data['count'], color='#ec9b99')
        plt.xlabel('Words', color='white')
        plt.ylabel('Count', color='white')
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.title('Most Common Words in NYT Headlines', color='white')
        plt.tight_layout()

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        plot_path = os.path.join(self.output_dir, f"common_words_plot_{self.current_date}.png")
        plt.savefig(plot_path, facecolor=fig.get_facecolor())
        print(f"Plot saved to {plot_path}")

    def run(self):
        data = self.load_data()
        self.generate_chart(data)

if __name__ == '__main__':
    csv_dir = r"C:\Projekty\NYT\data"
    output_dir = os.path.join(os.path.dirname(__file__), '../plots')

    generator = BarChartGenerator(csv_dir, output_dir)
    generator.run()
