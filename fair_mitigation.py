import pandas as pd
import sqlite3
from fairlearn.preprocessing import CorrelationRemover
from fairlearn.metrics import MetricFrame, selection_rate

# 1. Load the "Contaminated" Data
conn = sqlite3.connect('audit.db')
df = pd.read_sql_query("SELECT * FROM bookings", conn)

print("🚀 Starting Algorithmic Surgery...")

# 2. Setup the "Surgical Tools"
# We want to remove the correlation between 'device_type' and the prices
# First, we need to convert categorical device types to numbers for the math engine
df['device_encoded'] = df['device_type'].map({'Android': 0, 'Windows': 1, 'iPhone': 2, 'Mac': 3})

# Define our features
X = df[['base_price', 'device_encoded']]
sensitive_feature = df[['device_encoded']]

# 3. Perform Correlation Removal
# This 'removes' the influence of the sensitive feature from the dataset
cr = CorrelationRemover(sensitive_feature_ids=['device_encoded'], alpha=1.0)
X_transformed = cr.fit_transform(X)

# The transformed data gives us a "Fair Price" estimate
# (Simplified for our simulation)
df['fair_price'] = X_transformed[:, 0] # Taking the adjusted base price

# 4. Audit the "Fixed" Data
df['is_high_price_fixed'] = df['fair_price'] > 350

mf_fixed = MetricFrame(
    metrics={'Selection Rate (Fair)': selection_rate},
    y_true=df['is_high_price_fixed'],
    y_pred=df['is_high_price_fixed'],
    sensitive_features=df['device_type']
)

# 5. The Final Report
print("\n" + "="*40)
print("✅ POST-SURGERY FAIRNESS REPORT")
print("="*40)
print(mf_fixed.by_group)

sr_fixed = mf_fixed.by_group['Selection Rate (Fair)']
new_bias_ratio = sr_fixed.max() / (sr_fixed.min() if sr_fixed.min() > 0 else 0.01)

print("-" * 40)
print(f"📉 New Bias Ratio: {new_bias_ratio:.2f}")

if new_bias_ratio <= 1.10:
    print("🎊 SUCCESS: The algorithm is now COMPLIANT!")
else:
    print("⚠️ WARNING: Residual bias detected. Further tuning needed.")

conn.close()