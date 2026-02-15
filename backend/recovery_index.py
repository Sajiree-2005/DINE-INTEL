import pandas as pd
import os

# Paths
SENTIMENT_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\sentiment_per_customer.csv"
DELIVERY_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\delivery_per_customer.csv"
CHURN_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\churn_predictions.csv"
OUTPUT_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data\recovery_index.csv"

print("Loading sentiment, delivery, and churn data...")

# Load CSVs
df_sentiment = pd.read_csv(SENTIMENT_PATH)
df_delivery = pd.read_csv(DELIVERY_PATH)
df_churn = pd.read_csv(CHURN_PATH)

# Merge data
df = df_sentiment.merge(df_delivery, on="Customer_ID", how="outer") \
                 .merge(df_churn, on="Customer_ID", how="outer")

# -------------------------------
# 1. Sentiment Score (0 to 100)
# -------------------------------
df['Sentiment_Score'] = ((df['Avg_Sentiment'] + 1) / 2) * 100

# -------------------------------
# 2. Delivery Score (0 to 100)
# -------------------------------
df['Delivery_Score'] = 100 - (df['Avg_Delivery_Min'] / df['Avg_Delivery_Min'].max() * 100)

# -------------------------------
# 3. Churn Score (invert churn probability)
# -------------------------------
df['Churn_Score'] = (1 - df['Churn_Probability']) * 100

# -------------------------------
# 4. Recovery Index (average of 3 metrics)
# -------------------------------
df['Recovery_Index'] = df[['Sentiment_Score', 'Delivery_Score', 'Churn_Score']].mean(axis=1)

# Save final CSV
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Recovery index saved to {OUTPUT_PATH}")
