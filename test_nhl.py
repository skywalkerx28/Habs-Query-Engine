import pandas as pd

df = pd.read_csv('mtl_games_2024/playsequence-20241009-NHL-TORvsMTL-20242025-20006.csv')
print(df.head())  # Preview first 5 rows
print(df['type'].value_counts().head())  # Top event types (e.g., passes, shots)





