import pandas as pd
import os

# ======================================
# CONFIGURATION
# ======================================
BASE_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data"
DATA_PATH = os.path.join(BASE_PATH, "cleaned_data.csv")

CUSTOMER_OUTPUT = os.path.join(BASE_PATH, "sentiment_per_customer.csv")
RESTAURANT_OUTPUT = os.path.join(BASE_PATH, "sentiment_per_restaurant.csv")
SUMMARY_OUTPUT = os.path.join(BASE_PATH, "sentiment_summary.csv")

# ======================================
# LOAD DATA
# ======================================
print("📥 Loading cleaned dataset...")
df = pd.read_csv(DATA_PATH)

# Check required columns
required_cols = ['Customer_ID', 'Restaurant_Name', 'Review', 'Delivery_Rating']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing column: {col}")

# ======================================
# CLEAN AND CONVERT TO NUMERIC
# ======================================
print("🔧 Cleaning Review and Delivery_Rating columns...")

# Remove spaces, convert to numeric, replace NaN with neutral 3
df['Review'] = pd.to_numeric(df['Review'].astype(str).str.strip(), errors='coerce').fillna(3)
df['Delivery_Rating'] = pd.to_numeric(df['Delivery_Rating'].astype(str).str.strip(), errors='coerce').fillna(3)

# ======================================
# SENTIMENT CALCULATION
# ======================================
print("🧠 Calculating sentiment metrics...")

# Map 1–5 scale to -1 → +1
df['Review_Sentiment'] = (df['Review'] - 3) / 2
df['Delivery_Sentiment'] = (df['Delivery_Rating'] - 3) / 2

# Weighted combined sentiment (60% review, 40% delivery)
df['Combined_Sentiment'] = (0.6 * df['Review_Sentiment']) + (0.4 * df['Delivery_Sentiment'])

# ======================================
# SENTIMENT PER CUSTOMER
# ======================================
print("👤 Generating sentiment_per_customer.csv...")

sentiment_customer = df.groupby('Customer_ID').agg(
    Avg_Sentiment=('Combined_Sentiment', 'mean'),
    Num_Orders=('Customer_ID', 'count'),
    Avg_Review=('Review', 'mean'),
    Avg_Delivery_Rating=('Delivery_Rating', 'mean')
).reset_index()

sentiment_customer['Sentiment_Flag'] = sentiment_customer['Avg_Sentiment'].apply(
    lambda x: '⚠️ Negative' if x < -0.3 else ('✅ Positive' if x > 0.3 else '😐 Neutral')
)

sentiment_customer.to_csv(CUSTOMER_OUTPUT, index=False)
print(f"✅ Saved: {CUSTOMER_OUTPUT}")

# ======================================
# SENTIMENT PER RESTAURANT
# ======================================
print("🍴 Generating sentiment_per_restaurant.csv...")

sentiment_restaurant = df.groupby('Restaurant_Name').agg(
    Avg_Sentiment=('Combined_Sentiment', 'mean'),
    Num_Orders=('Restaurant_Name', 'count'),
    Avg_Review=('Review', 'mean'),
    Avg_Delivery_Rating=('Delivery_Rating', 'mean')
).reset_index()

sentiment_restaurant['Performance_Flag'] = sentiment_restaurant['Avg_Sentiment'].apply(
    lambda x: '🚨 Poor Experience' if x < -0.3 else ('🌟 Excellent Partner' if x > 0.3 else '🟡 Average')
)

sentiment_restaurant.to_csv(RESTAURANT_OUTPUT, index=False)
print(f"✅ Saved: {RESTAURANT_OUTPUT}")

# ======================================
# SUMMARY / ANOMALY SNAPSHOT
# ======================================
print("📊 Creating summary snapshot...")

summary = pd.DataFrame({
    'Metric': ['Total_Customers', 'Total_Restaurants', 'Negative_Customers', 'Negative_Restaurants'],
    'Count': [
        len(sentiment_customer),
        len(sentiment_restaurant),
        (sentiment_customer['Sentiment_Flag'] == '⚠️ Negative').sum(),
        (sentiment_restaurant['Performance_Flag'] == '🚨 Poor Experience').sum()
    ]
})

summary.to_csv(SUMMARY_OUTPUT, index=False)
print(f"✅ Summary saved: {SUMMARY_OUTPUT}")

print("\n🎉 Sentiment analysis complete!")
print("Generated files:")
print(f" - {CUSTOMER_OUTPUT}")
print(f" - {RESTAURANT_OUTPUT}")
print(f" - {SUMMARY_OUTPUT}")
