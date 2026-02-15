# backend/delivery_performance.py

import pandas as pd
import os

# -------------------------------
# Step 4: Delivery Performance Analysis
# -------------------------------

# Paths
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_DIR = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load cleaned data
print("Loading cleaned data...")
df = pd.read_csv(DATA_PATH)

# Ensure numeric types
df['Distance_in_km'] = pd.to_numeric(df['Distance_in_km'], errors='coerce').fillna(0)
df['Time_Taken_In_Min'] = pd.to_numeric(df['Time_Taken_In_Min'], errors='coerce').fillna(1)  # avoid division by zero

# -------------------------------
# 1. Average Delivery Time by Traffic
# -------------------------------
avg_time_traffic = df.groupby('Road_Traffic_Density')['Time_Taken_In_Min'].mean().reset_index()
avg_time_traffic.rename(columns={'Time_Taken_In_Min': 'Avg_Delivery_Time_Min'}, inplace=True)
avg_time_traffic.to_csv(os.path.join(OUTPUT_DIR, 'avg_delivery_time_traffic.csv'), index=False)
print("✅ Average delivery time by traffic saved")

# -------------------------------
# 2. Average Delivery Time by Weather
# -------------------------------
avg_time_weather = df.groupby('Weather_Conditions')['Time_Taken_In_Min'].mean().reset_index()
avg_time_weather.rename(columns={'Time_Taken_In_Min': 'Avg_Delivery_Time_Min'}, inplace=True)
avg_time_weather.to_csv(os.path.join(OUTPUT_DIR, 'avg_delivery_time_weather.csv'), index=False)
print("✅ Average delivery time by weather saved")

# -------------------------------
# 3. Delivery Time per Distance Bucket
# -------------------------------
bins = [0, 2, 5, 8, 12, 20, 50]
labels = ['0-2km', '2-5km', '5-8km', '8-12km', '12-20km', '20-50km']
df['Distance_Bucket'] = pd.cut(df['Distance_in_km'], bins=bins, labels=labels, right=False)

avg_time_distance = df.groupby('Distance_Bucket')['Time_Taken_In_Min'].mean().reset_index()
avg_time_distance.rename(columns={'Time_Taken_In_Min': 'Avg_Delivery_Time_Min'}, inplace=True)
avg_time_distance.to_csv(os.path.join(OUTPUT_DIR, 'avg_delivery_time_distance.csv'), index=False)
print("✅ Average delivery time by distance bucket saved")

# -------------------------------
# 4. Delivery Efficiency (Percentage)
# -------------------------------
# Raw efficiency (km per min)
df['Delivery_Efficiency'] = df['Distance_in_km'] / df['Time_Taken_In_Min']

# Convert to percentage relative to expected efficiency (0.5 km/min)
EXPECTED_EFFICIENCY = 0.5
df['Delivery_Efficiency_Percent'] = (df['Delivery_Efficiency'] / EXPECTED_EFFICIENCY * 100).clip(upper=100)

df[['Order_ID', 'Restaurant_ID', 'Distance_in_km', 'Time_Taken_In_Min', 
    'Delivery_Efficiency', 'Delivery_Efficiency_Percent']].to_csv(
    os.path.join(OUTPUT_DIR, 'delivery_efficiency.csv'), index=False
)
print("✅ Delivery efficiency per order saved (as % relative to standard)")

# -------------------------------
# 5. Delivery Performance per Customer
# -------------------------------
performance_customer = df.groupby('Customer_ID').agg(
    Avg_Delivery_Time=('Time_Taken_In_Min', 'mean'),
    Avg_Distance=('Distance_in_km', 'mean'),
    Avg_Efficiency_Percent=('Delivery_Efficiency_Percent', 'mean'),
    Total_Orders=('Order_ID', 'count')
).reset_index()
performance_customer.to_csv(os.path.join(OUTPUT_DIR, 'delivery_per_customer.csv'), index=False)
print("✅ Delivery performance per customer saved")

# -------------------------------
# 6. Delivery Performance per Phase
# -------------------------------
performance_phase = df.groupby('Phase').agg(
    Avg_Delivery_Time=('Time_Taken_In_Min', 'mean'),
    Avg_Distance=('Distance_in_km', 'mean'),
    Avg_Efficiency_Percent=('Delivery_Efficiency_Percent', 'mean'),
    Total_Orders=('Order_ID', 'count')
).reset_index()
performance_phase.to_csv(os.path.join(OUTPUT_DIR, 'delivery_per_phase.csv'), index=False)
print("✅ Delivery performance per phase saved")

print("✅ Delivery Performance Analysis Completed!")
