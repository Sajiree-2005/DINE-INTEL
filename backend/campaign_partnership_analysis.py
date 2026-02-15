# backend/campaign_partnership_analysis.py

import pandas as pd
import os

# -------------------------------
# Step 5: Campaign & Partnership Analysis
# -------------------------------

# Paths
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_CAMPAIGN = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\campaign_analysis.csv"
OUTPUT_PARTNER = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\partner_analysis.csv"

# Load cleaned data
print("Loading cleaned data...")
df = pd.read_csv(DATA_PATH)

# -------------------------------
# 1. Campaign Analysis
# -------------------------------
# Keep relevant columns
campaign_df = df[['Campaign_Name', 'Phase', 'Order_ID']].copy()
campaign_df['Campaign_Name'].fillna('No Campaign', inplace=True)

# Aggregate number of orders per campaign per phase
campaign_metrics = campaign_df.groupby(['Campaign_Name', 'Phase'])['Order_ID'].count().reset_index()
campaign_metrics.rename(columns={'Order_ID': 'Total_Orders'}, inplace=True)

# Save CSV
os.makedirs(os.path.dirname(OUTPUT_CAMPAIGN), exist_ok=True)
campaign_metrics.to_csv(OUTPUT_CAMPAIGN, index=False)
print(f"✅ Campaign analysis saved to {OUTPUT_CAMPAIGN}")

# -------------------------------
# 2. Partner / Restaurant Analysis
# -------------------------------
# Keep relevant columns
partner_df = df[['Restaurant_Name', 'Phase', 'Order_ID', 'Total']].copy()

# Aggregate metrics per restaurant per phase
partner_metrics = partner_df.groupby(['Restaurant_Name', 'Phase']).agg(
    Total_Orders=('Order_ID', 'count'),
    Total_Revenue=('Total', 'sum')
).reset_index()

# Identify top restaurants (high order count + revenue)
partner_metrics['Rank'] = partner_metrics.groupby('Phase')['Total_Revenue'].rank(ascending=False, method='first')

# Save CSV
partner_metrics.to_csv(OUTPUT_PARTNER, index=False)
print(f"✅ Partner / Restaurant analysis saved to {OUTPUT_PARTNER}")

print("✅ Campaign & Partnership Analysis Completed!")
