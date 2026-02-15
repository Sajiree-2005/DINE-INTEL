# backend/order_patterns.py

import pandas as pd
import os

# -------------------------------
# Step 3: Order Patterns Analysis
# -------------------------------

# Paths
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_PATH_PHASE = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\order_patterns_phase.csv"
OUTPUT_PATH_CITY = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\order_patterns_city.csv"
OUTPUT_PATH_RESTAURANT = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\order_patterns_restaurant.csv"

# Load cleaned data
print("Loading cleaned data...")
df = pd.read_csv(DATA_PATH)

# -------------------------------
# 1. Orders per Phase
# -------------------------------
orders_phase = df.groupby('Phase')['Order_ID'].count().reset_index()
orders_phase.rename(columns={'Order_ID': 'Total_Orders'}, inplace=True)

# Save phase-level data
os.makedirs(os.path.dirname(OUTPUT_PATH_PHASE), exist_ok=True)
orders_phase.to_csv(OUTPUT_PATH_PHASE, index=False)
print(f"✅ Orders per Phase saved to {OUTPUT_PATH_PHASE}")

# -------------------------------
# 2. Orders per City per Phase
# -------------------------------
orders_city = df.groupby(['City', 'Phase'])['Order_ID'].count().reset_index()
orders_city.rename(columns={'Order_ID': 'Total_Orders'}, inplace=True)

# Save city-level data
orders_city.to_csv(OUTPUT_PATH_CITY, index=False)
print(f"✅ Orders per City per Phase saved to {OUTPUT_PATH_CITY}")

# -------------------------------
# 3. Orders per Restaurant per Phase
# -------------------------------
# Using Place_Name instead of Restaurant_Name
orders_restaurant = df.groupby(['Place_Name', 'Phase'])['Order_ID'].count().reset_index()
orders_restaurant.rename(columns={'Order_ID': 'Total_Orders'}, inplace=True)

# Save restaurant-level data
orders_restaurant.to_csv(OUTPUT_PATH_RESTAURANT, index=False)
print(f"✅ Orders per Restaurant per Phase saved to {OUTPUT_PATH_RESTAURANT}")

print("✅ Order Patterns Analysis Completed!")
