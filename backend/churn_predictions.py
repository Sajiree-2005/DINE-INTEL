# backend/churn_predictions.py
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# ----------------------------
# Step 1: Load processed data
# ----------------------------
df = pd.read_csv("processed_data/cleaned_data.csv")
print(f"Loaded data: {df.shape}")

# ----------------------------
# Step 2: Generate churn label
# Example logic: churn if customer did not order in last phase
# ----------------------------
# Count number of orders per customer in last phase
last_phase = 'Recovery'  # adjust if phases are named differently
phase_orders = df[df['Phase'] == last_phase].groupby('Customer_ID')['Order_ID'].count().reset_index()
phase_orders.rename(columns={'Order_ID':'Orders_Last_Phase'}, inplace=True)

# Merge with main df (one row per customer)
df_customers = df[['Customer_ID']].drop_duplicates().merge(phase_orders, on='Customer_ID', how='left')
df_customers['Orders_Last_Phase'] = df_customers['Orders_Last_Phase'].fillna(0)

# Churn logic: 1 = churn, 0 = active
df_customers['Churn_Next_Week'] = df_customers['Orders_Last_Phase'].apply(lambda x: 1 if x == 0 else 0)
print("Churn label distribution:")
print(df_customers['Churn_Next_Week'].value_counts())

# ----------------------------
# Step 3: Prepare features
# Example features: adjust as per your dataset
# ----------------------------
# Aggregate customer-level metrics
agg = df.groupby('Customer_ID').agg({
    'Order_ID':'count',
    'Total':'mean',
    'Time_Taken_In_Min':'mean',
    'Sentiment_Score':'mean'
}).reset_index()
agg.rename(columns={
    'Order_ID':'Order_Count',
    'Total':'Avg_Order_Value',
    'Time_Taken_In_Min':'Avg_Delivery_Delay',
    'Sentiment_Score':'Avg_Sentiment'
}, inplace=True)

# Merge features with churn label
df_model = df_customers.merge(agg, on='Customer_ID', how='left')

# ----------------------------
# Step 4: Train XGBoost classifier
# ----------------------------
X = df_model[['Order_Count','Avg_Order_Value','Avg_Delivery_Delay','Avg_Sentiment']]
y = df_model['Churn_Next_Week']

# Ensure at least two classes
if len(y.unique()) < 2:
    raise ValueError("Churn label has only one class. Adjust churn generation logic.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# ----------------------------
# Step 5: Predict churn probability
# ----------------------------
df_model['Churn_Probability'] = model.predict_proba(X)[:,1]

# ----------------------------
# Step 6: Save predictions
# ----------------------------
df_model[['Customer_ID','Churn_Probability']].to_csv("processed_data/churn_predictions.csv", index=False)
print("✅ Churn predictions saved to processed_data/churn_predictions.csv")
