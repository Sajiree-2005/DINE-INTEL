# backend/process_data.py

import pandas as pd
from textblob import TextBlob
import os

# -------- CONFIG --------
DATA_PATH = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\data\FoodTech_Dataset.xlsx"
OUTPUT_DIR = r"C:\Users\SAJIREE\OneDrive\Desktop\Projects\Food-Tech Startup\processed_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------- LOAD DATA --------
print("Loading Excel file...")
df = pd.read_excel(DATA_PATH)
print(f"Initial data shape: {df.shape}")

# -------- BASIC CLEANING --------
print("Cleaning data...")

# Rename Customer_I -> Customer_ID for consistency
if "Customer_I" in df.columns:
    df.rename(columns={"Customer_I": "Customer_ID"}, inplace=True)

# Drop rows with missing critical IDs
df.dropna(subset=["Order_ID", "Restaurant_ID", "Customer_ID"], inplace=True)

# Fill missing Reviews
df["Review"].fillna("No Review", inplace=True)

# Convert date/time columns
df["Time_Ordered"] = pd.to_datetime(df["Time_Ordered"], errors='coerce')
df["Time_Order_Picked"] = pd.to_datetime(df["Time_Order_Picked"], errors='coerce')

# Convert numeric columns
numeric_cols = ["Delivery_Rating", "Delivery_Person_Ratings", "Total", "Discount", "Time_Taken_In_Min", "Distance"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# -------- DERIVED METRICS --------
print("Calculating delivery delays...")
df["Delivery_Delay_Min"] = (df["Time_Order_Picked"] - df["Time_Ordered"]).dt.total_seconds() / 60
df["Delivery_Delay_Min"].fillna(0, inplace=True)

df["Effective_Discount_%"] = (df["Discount"] / df["Total"] * 100).fillna(0)

# -------- SENTIMENT ANALYSIS --------
print("Performing sentiment analysis...")
def get_sentiment(text):
    return TextBlob(str(text)).sentiment.polarity

df["Sentiment_Score"] = df["Review"].apply(get_sentiment)
df["Sentiment_Label"] = df["Sentiment_Score"].apply(
    lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")
)

# -------- AGGREGATE SENTIMENT --------
print("Aggregating sentiment per customer and per restaurant...")
sentiment_customer = df.groupby('Customer_ID').agg(Avg_Sentiment=('Sentiment_Score', 'mean')).reset_index()
sentiment_restaurant = df.groupby('Restaurant_ID').agg(Avg_Sentiment=('Sentiment_Score', 'mean')).reset_index()

# -------- SAVE PROCESSED FILES --------
cleaned_csv = os.path.join(OUTPUT_DIR, "cleaned_data.csv")
sentiment_csv = os.path.join(OUTPUT_DIR, "sentiment_data.csv")
sentiment_customer_csv = os.path.join(OUTPUT_DIR, "sentiment_per_customer.csv")
sentiment_restaurant_csv = os.path.join(OUTPUT_DIR, "sentiment_per_restaurant.csv")

print(f"Saving cleaned data to {cleaned_csv}...")
df.to_csv(cleaned_csv, index=False)
print(f"Saving sentiment data to {sentiment_csv}...")
df.to_csv(sentiment_csv, index=False)
print(f"Saving sentiment per customer to {sentiment_customer_csv}...")
sentiment_customer.to_csv(sentiment_customer_csv, index=False)
print(f"Saving sentiment per restaurant to {sentiment_restaurant_csv}...")
sentiment_restaurant.to_csv(sentiment_restaurant_csv, index=False)

print("✅ Data processing complete!")
