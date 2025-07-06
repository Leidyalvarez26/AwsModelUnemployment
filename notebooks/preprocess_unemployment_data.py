import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
import os

# 📍 Load wide-form dataset
data_path = "/home/alejandroramirez/Documents/unemploymentML/data/unemployment_rates.csv"
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

# 📦 Save full processed dataset with headers (for inspection)
processed_path = Path("/home/alejandroramirez/Documents/unemploymentML/data/processed_unemployment_data.csv")
processed_path.parent.mkdir(parents=True, exist_ok=True)
df_long.to_csv(processed_path, index=False)

print(f"✅ Full processed dataset saved to {processed_path}")

# 📦 Create numeric-only CSV without header for SageMaker
df_numeric = df_long[['Unemployment Rate', 'Year', 'Month', 'Quarter', 'Region Code']]

sagemaker_input_path = Path("/home/alejandroramirez/Documents/unemploymentML/data/sagemaker_input_data.csv")
df_numeric.to_csv(sagemaker_input_path, index=False, header=False)

print(f"✅ Numeric-only CSV for SageMaker saved to {sagemaker_input_path}")
