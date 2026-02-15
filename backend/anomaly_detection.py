import pandas as pd
import os

# Paths
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\anomaly_report.csv"

# Load dataset
print("Loading cleaned data...")
df = pd.read_csv(DATA_PATH)

# Convert time columns to datetime
df['Time_Ordered'] = pd.to_datetime(df['Time_Ordered'], errors='coerce')
df['Time_Order_Picked'] = pd.to_datetime(df['Time_Order_Picked'], errors='coerce')

# Calculate delivery duration in minutes
df['Delivery_Duration'] = (df['Time_Order_Picked'] - df['Time_Ordered']).dt.total_seconds() / 60
df['Delivery_Duration'] = df['Delivery_Duration'].fillna(0)

# Initialize anomaly flags
df['Anomaly_Type'] = ""

# 1️⃣ Delivery Duration anomalies
avg_duration = df['Delivery_Duration'].mean()
std_duration = df['Delivery_Duration'].std()
df.loc[df['Delivery_Duration'] > avg_duration + 3*std_duration, 'Anomaly_Type'] += "Long Delivery; "
df.loc[df['Delivery_Duration'] < 0, 'Anomaly_Type'] += "Negative Delivery; "

# 2️⃣ Order total / discount anomalies
avg_total = df['Total'].mean()
std_total = df['Total'].std()
df.loc[df['Total'] > avg_total + 3*std_total, 'Anomaly_Type'] += "High Total; "
df.loc[df['Total'] < avg_total - 3*std_total, 'Anomaly_Type'] += "Low Total; "

# 3️⃣ Delivery person ratings anomalies
df.loc[df['Delivery_Person_Ratings'] < 2.5, 'Anomaly_Type'] += "Low Delivery Rating; "

# 4️⃣ Order status anomalies
df.loc[df['Order_Status'].isin(['Lost', 'Cancelled', 'Returned']), 'Anomaly_Type'] += "Problematic Order; "

# Keep only rows with anomalies
anomalies = df[df['Anomaly_Type'] != ""]

# Save CSV
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
anomalies.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Anomaly detection report saved to {OUTPUT_PATH}")
