import pandas as pd
import sqlite3
from fairlearn.metrics import MetricFrame, selection_rate

# 1. Database Connection (Accessing the "Medical Records" of our AI)
try:
    conn = sqlite3.connect('audit.db')
    df = pd.read_sql_query("SELECT * FROM bookings", conn)
    print(f"🏥 Audit Lab: Successfully loaded {len(df)} records.")
except Exception as e:
    print(f"❌ Error: Could not connect to database. {e}")
    exit()

# 2. Define "High Price" Event
# We define a 'High Price' as any booking over 350 EUR.
# This helps us track if certain groups are 'selected' for high prices more often.
df['is_high_price'] = df['final_price'] > 350

# 3. Fairness Assessment via Fairlearn
# We use 'selection_rate' to see the percentage of users getting high prices.
metrics = {
    'Selection Rate (High Price)': selection_rate
}

mf = MetricFrame(
    metrics=metrics,
    y_true=df['is_high_price'],  # Ground truth (not used for logic, just required by API)
    y_pred=df['is_high_price'],  # The actual outcomes we are auditing
    sensitive_features=df['device_type']
)

# 4. Generate Audit Report
print("\n" + "="*40)
print("🩺 FAIRLEARN CLINICAL AUDIT REPORT")
print("="*40)
print(mf.by_group)

# 5. Calculate Disparate Impact Ratio
# The ratio between the group receiving the most high prices vs the least.
sr = mf.by_group['Selection Rate (High Price)']
bias_ratio = sr.max() / (sr.min() if sr.min() > 0 else 0.01)

print("-" * 40)
print(f"📈 Calculated Bias Ratio: {bias_ratio:.2f}")

# 6. Compliance Gate Logic
THRESHOLD = 1.10
if bias_ratio > THRESHOLD:
    print(f"🚨 STATUS: NON-COMPLIANT (Ratio {bias_ratio:.2f} > {THRESHOLD})")
    print("ACTION: Immediate mitigation required. Algorithm shows bias against specific devices.")
else:
    print(f"✅ STATUS: COMPLIANT (Ratio {bias_ratio:.2f} <= {THRESHOLD})")
    print("ACTION: System is within legal safety limits.")

conn.close()