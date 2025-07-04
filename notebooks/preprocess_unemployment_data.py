import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 📍 Load long-form dataset (after melt)
data_path = "../data/unemployment_rates.csv"
df = pd.read_csv(data_path)

# 📊 Melt wide table to long
value_vars = df.columns[5:]
df_long = pd.melt(df,
                  id_vars=['Region Name'],
                  value_vars=value_vars,
                  var_name='Date',
                  value_name='Unemployment Rate')

# 📅 Convert Date
df_long['Date'] = pd.to_datetime(df_long['Date'])

# 🎛️ Feature engineering
df_long['Year'] = df_long['Date'].dt.year
df_long['Month'] = df_long['Date'].dt.month
df_long['Quarter'] = df_long['Date'].dt.quarter

# 🎛️ Encode Region Name
le = LabelEncoder()
df_long['Region Code'] = le.fit_transform(df_long['Region Name'])

# 🧹 Handle missing values
df_long.dropna(subset=['Unemployment Rate'], inplace=True)

# 📦 Save cleaned dataset
df_long.to_csv("../data/processed_unemployment_data.csv", index=False)

print("✅ Preprocessing complete. Processed dataset saved.")
