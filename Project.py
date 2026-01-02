import requests
import json
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# API URL
url = "https://data.covid19india.org/data.json"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    print("✅ Data fetched from API")
except Exception as e:
    print("❌ Failed to fetch data from API:", e)
    # Sample fallback JSON (for demo)
    data = {
        "statewise": [
            {"state": "Gujarat", "confirmed": "1250000", "active": "4500", "recovered": "1230000", "deaths": "15000"},
            {"state": "Maharashtra", "confirmed": "2400000", "active": "6000", "recovered": "2370000", "deaths": "30000"},
            {"state": "Delhi", "confirmed": "1800000", "active": "2000", "recovered": "1780000", "deaths": "12000"},
            {"state": "Karnataka", "confirmed": "1500000", "active": "3000", "recovered": "1470000", "deaths": "20000"},
            {"state": "Tamil Nadu", "confirmed": "1400000", "active": "2500", "recovered": "1380000", "deaths": "17500"},
            {"state": "Total", "confirmed": "10000000", "active": "20000", "recovered": "9900000", "deaths": "50000"},
        ]
    }
    print("✅ Loaded fallback sample data")

# Convert to DataFrame
state_data = data['statewise']
df = pd.DataFrame(state_data)
df = df[['state', 'confirmed', 'active', 'recovered', 'deaths']]
df[['confirmed', 'active', 'recovered', 'deaths']] = df[['confirmed', 'active', 'recovered', 'deaths']].astype(int)

print("\n🔹 Sample Data:\n", df.head())

# Store to SQLite
conn = sqlite3.connect('covid_data.db')
df.to_sql('covid_stats', conn, if_exists='replace', index=False)
print("\n✅ Data saved to SQLite")

# Query from SQLite
df_sql = pd.read_sql_query("SELECT * FROM covid_stats WHERE state != 'Total'", conn)
conn.close()

# NumPy stats
confirmed_array = np.array(df_sql['confirmed'])
print("\n📊 NumPy Stats:")
print("Average Confirmed:", np.mean(confirmed_array))
print("Max Confirmed:", np.max(confirmed_array))
print("Min Confirmed:", np.min(confirmed_array))

# Plot with matplotlib
top10 = df_sql.sort_values(by='confirmed', ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top10['state'], top10['confirmed'], color='green')
plt.title('Top 10 States by Confirmed COVID-19 Cases')
plt.xlabel('States')
plt.ylabel('Confirmed Cases')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()