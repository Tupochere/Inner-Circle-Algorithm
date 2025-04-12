import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend suitable for headless environments
from strategies.structure_detector import detect_market_structure

# Get historical 1H candles
df = yf.download('EURUSD=X', interval='1h', period='5d', auto_adjust=False)

# Flatten multi-index columns
df.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
df.reset_index(inplace=True)
df.rename(columns={"Datetime": "timestamp"}, inplace=True)

# Ensure timestamp is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Print the first few rows of the dataframe
print(df.head())

# Detect structure
market_structure = detect_market_structure(df)

# Print result
for timestamp, label in market_structure:
    print(f"{timestamp} → {label}")


def plot_market_structure(df, structure_points):
    plt.figure(figsize=(18, 8))  # Increase figure size
    plt.plot(df['timestamp'], df['close'], label='Close Price', color='black')

    for ts, label in structure_points:
        x = df[df['timestamp'] == ts].index[0]
        y = df['close'][x]

        color = {
            'HH': 'green',
            'LL': 'red',
            'BOS': 'blue',
            'CHoCH': 'orange'
        }.get(label, 'gray')

        plt.scatter(df['timestamp'][x], y, label=label, color=color)
        plt.text(df['timestamp'][x], y, label, fontsize=9, color=color)

    plt.title("ICT Market Structure")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 1, 0.9])  # Adjust rect parameter to leave more space

    try:
        plt.show()
    except Exception as e:
        print(f"Error displaying plot: {e}. Saving plot as 'market_structure.png'.")
        plt.savefig('market_structure.png')

plot_market_structure(df, market_structure)
plt.savefig('market_structure.png')
print("✅ Chart saved as market_structure.png. You can view it in the file explorer or download it.")
# Save the plot to a file

plt.close()  # Close the plot to free up memory
