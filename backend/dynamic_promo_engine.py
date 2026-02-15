import pandas as pd
import os

# ---------------- Paths ----------------
ORDERS_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\cleaned_data.csv"
OUTPUT_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\dynamic_promos.csv"

# ---------------- Load Data ----------------
df = pd.read_csv(ORDERS_PATH)

# Fill missing values
df['Order_Status'].fillna('Delivered', inplace=True)
df['Discount'] = df['Discount'].fillna(0)
df['Sentiment_Score'] = df.get('Sentiment_Score', 0)  # if missing, fill with 0
df['Total'] = df.get('Total', 0)                        # if missing, fill with 0

# Count abandoned/lost orders per customer
abandoned_counts = (
    df[df['Order_Status'].isin(['Lost', 'Cancelled', 'Returned'])]
    .groupby('Customer_ID')
    .size()
    .reset_index(name='Abandoned_Count')
)

# Aggregate sentiment and total spend per customer
customer_agg = df.groupby('Customer_ID').agg({
    'Sentiment_Score': 'mean',  # average sentiment
    'Total': 'sum'               # total spend
}).reset_index()

# Merge all customer info
df_customers = df[['Customer_ID']].drop_duplicates()
df_customers = df_customers.merge(abandoned_counts, on='Customer_ID', how='left')
df_customers = df_customers.merge(customer_agg, on='Customer_ID', how='left')

# Fill missing values
df_customers['Abandoned_Count'].fillna(0, inplace=True)
df_customers['Sentiment_Score'].fillna(0, inplace=True)
df_customers['Total'].fillna(0, inplace=True)

# ---------------- Dynamic Promo Logic ----------------
def suggest_promo(row):
    if row['Abandoned_Count'] >= 2:
        return "10% Off - Cart Abandoner"
    elif row['Sentiment_Score'] < -0.2:
        return "Free Delivery - Low Sentiment"
    elif row['Total'] > 1000:
        return "Exclusive 15% Off - VIP"
    else:
        return "Standard Promo"

df_customers['Promo_Suggestion'] = df_customers.apply(suggest_promo, axis=1)

# ---------------- Save Output ----------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df_customers.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Dynamic promo suggestions saved to {OUTPUT_PATH}")
