import pandas as pd
import os

# === Paths ===
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\campaign_recommendations.csv"

print("📊 Loading processed datasets for campaign recommendations...")

# === Load Dataset ===
df = pd.read_csv(DATA_PATH)

# === Clean Columns ===
df.columns = df.columns.str.strip()

# === Basic Cleaning ===
df['Review'] = pd.to_numeric(df['Review'], errors='coerce').fillna(0)
df['Delivery_Person_Ratings'] = pd.to_numeric(df['Delivery_Person_Ratings'], errors='coerce').fillna(0)
df['Time_Taken_In_Min'] = pd.to_numeric(df['Time_Taken_In_Min'], errors='coerce').fillna(0)
df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0)
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)

# === Compute performance metrics per restaurant ===
restaurant_perf = df.groupby('Restaurant_ID').agg(
    Avg_Review=('Review', 'mean'),
    Avg_Delivery_Rating=('Delivery_Person_Ratings', 'mean'),
    Avg_Delivery_Time=('Time_Taken_In_Min', 'mean'),
    Avg_Discount=('Discount', 'mean'),
    Total_Revenue=('Total', 'sum'),
    Num_Orders=('Order_ID', 'count'),
).reset_index()

# === Campaign Suitability Score ===
# Weighted formula: higher review & rating + more orders, less delivery time
restaurant_perf['Campaign_Score'] = (
    (restaurant_perf['Avg_Review'] * 0.3) +
    (restaurant_perf['Avg_Delivery_Rating'] * 0.4) +
    (restaurant_perf['Num_Orders'] * 0.2) -
    (restaurant_perf['Avg_Delivery_Time'] * 0.1)
)

# === Recommend Campaign Type ===
def recommend_campaign(row):
    if row['Avg_Review'] >= 4 and row['Avg_Delivery_Rating'] >= 4.5:
        return "⭐ Premium Partnership Campaign"
    elif row['Avg_Review'] >= 3.5:
        return "🎯 Discount Boost Campaign"
    elif row['Avg_Delivery_Time'] > 40:
        return "⚡ Speed Optimization Campaign"
    else:
        return "💬 Customer Engagement Campaign"

restaurant_perf['Recommended_Campaign'] = restaurant_perf.apply(recommend_campaign, axis=1)

# === Sort by Campaign Score ===
restaurant_perf = restaurant_perf.sort_values(by='Campaign_Score', ascending=False)

# === Save Output ===
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
restaurant_perf.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Campaign recommendations saved to {OUTPUT_PATH}")
