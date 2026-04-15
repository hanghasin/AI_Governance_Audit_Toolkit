import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# 1. Initialize Database Connection
# We are auditing the "audit.db" created in previous sessions
conn = sqlite3.connect('audit.db')
df = pd.read_sql_query("SELECT * FROM bookings", conn)

print("📊 Initializing XAI (Explainable AI) Engine...")

# 2. Data Preparation for Analysis
# We map device types to numerical values to allow the model to calculate weights
df['device_encoded'] = df['device_type'].map({
    'Android': 0, 
    'Windows': 1, 
    'iPhone': 2, 
    'Mac': 3
})

# Define Features (Independent Variables) and Target (Dependent Variable)
X = df[['base_price', 'device_encoded']]
y = df['final_price']

# 3. Train the Explainer Model (Random Forest)
# Random Forest is ideal for XAI as it provides "Feature Importance" metrics
explainer = RandomForestRegressor(n_estimators=100, random_state=42)
explainer.fit(X, y)

# 4. Extract Feature Importances
importances = explainer.feature_importances_
feature_names = ['Market Price (Legal)', 'Device Identifier (Proxy)']

# 5. Visual Transparency Report
plt.figure(figsize=(10, 6))
colors = ['#4CAF50', '#FF5722'] # Green for legal factor, Orange for bias risk factor

plt.bar(feature_names, importances, color=colors)
plt.title('🛡️ Algorithm Transparency: Pricing Drivers Analysis')
plt.ylabel('Contribution to Pricing Decision (0.0 - 1.0)')
plt.ylim(0, 1.1)

# Annotate bars with precise values
for i, v in enumerate(importances):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center', fontweight='bold')

# Save the diagnostic image
plt.savefig('xai_report.png')
print("✅ Success: Transparency Report saved as 'xai_report.png'")

conn.close()