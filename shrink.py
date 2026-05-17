import pandas as pd

df = pd.read_csv('flights.csv', nrows=10000)
df.to_csv('flights.csv', index=False)

print(f"Done! Saved {len(df)} rows")