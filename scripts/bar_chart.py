import pandas as pd
import os
import datetime

import matplotlib.pyplot as plt

# Load DataFrame from CSV file
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
csv_path = os.path.join(os.path.dirname(__file__), f"../data/common_words_{current_date}.csv")
common_words_df = pd.read_csv(csv_path)
# Filter for the top 10 most common words
common_words_df = common_words_df.nlargest(10, 'count')
# Generate a bar chart with a darker background
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#232136')  # Set the background color for the entire figure
ax.set_facecolor('#232136')  # Set the background color for the chart area

plt.bar(common_words_df['word'], common_words_df['count'], color='#ec9b99')
plt.xlabel('Words', color='white')
plt.ylabel('Count', color='white')
plt.xticks(rotation=45, color='white')
plt.yticks(color='white')
plt.title('Most Common Words in NYT Headlines', color='white')
plt.tight_layout()

# Save the chart to a PNG file in the `plots` directory
plots_dir = os.path.join(os.path.dirname(__file__), f"../plots")
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
plot_path = os.path.join(plots_dir, f"common_words_plot_{current_date}.png")

# Save the chart to a PNG file with a dark background
plt.savefig(plot_path, facecolor=fig.get_facecolor())

plt.savefig(plot_path)

print(f"Plot saved to {plot_path}")
