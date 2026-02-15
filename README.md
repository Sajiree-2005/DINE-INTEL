# 🍽️ DINE-INTEL  
### AI-Powered Operational Recovery & Customer Intelligence Platform

DINE-INTEL is an intelligent analytics and recovery platform built for food-tech businesses.  
It transforms delivery, customer, and campaign data into actionable insights using AI-driven monitoring and real-time dashboards.

---

## 🚀 Problem Statement

Food-tech businesses often struggle with:

- Delivery delays
- Rising order cancellations
- Negative customer reviews
- Customer churn
- Ineffective marketing campaigns

Most platforms only track data — they don’t provide intelligent recovery strategies.

**DINE-INTEL bridges that gap.**

---

## 💡 Solution Overview

DINE-INTEL integrates:

- 📦 Delivery Intelligence  
- 👥 Customer Intelligence  
- 📊 Recovery Metrics  
- 🎯 Smart Campaign Recommendations  
- 🤖 Interactive AI Chatbot  

The platform converts raw operational data into meaningful recovery strategies.

---

## ✨ Key Features

### 📦 Delivery Intelligence
- Delivery Success Rate Monitoring  
- SLA Tracking & Compliance  
- Delivery Heatmap Insights  
- Real-Time Delay Detection  

### 👥 Customer Intelligence
- Customer Segmentation  
- At-Risk Customer Detection  
- Churn Monitoring  
- Loyalty & Retention Insights  

### 🎯 Campaign Engine
- Personalized Campaign Recommendations  
- Dynamic Promo Engine  
- Promotion Performance Tracking  

### 📊 Recovery Dashboard
- Recovery Index Metric  
- Order Trend Analysis (Pre-Crisis → Crisis → Recovery)  
- Anomaly Detection System  
- Real-Time Performance Monitoring  

### 🤖 DINE-INTEL Chatbot
- Web-based interactive chatbot  
- Keyword-based knowledge engine  
- Typing animation  
- Scroll animations  
- Smart fallback response:
  > "I don’t understand. Please contact a DINE-INTEL employee for assistance."

---

## 🛠️ Tech Stack

### Frontend
- HTML5  
- CSS3  
- JavaScript  
- LocalStorage (Chat Toggle Persistence)  
- Scroll Animations  

### Backend
- Python  
- Flask  

### Other Components
- JSON API communication  
- Knowledge Base (`knowledge_base.py`)  

---

## 🧠 How the Chatbot Works

1. User enters a query.
2. Message is sent to the Flask `/chatbot` endpoint.
3. Backend checks `knowledge_base.py` for keyword matches.
4. If match found → intelligent response returned.
5. If no match → fallback message suggesting employee contact.

---

## 📂 Project Structure


---

## ▶️ How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/dine-intel.git
```
```bash
2️⃣ Navigate into the Folder
cd dine-intel
```
```bash
3️⃣ Install Dependencies
pip install flask
```
```bash
4️⃣ Run the Application
python app.py
```
