import pandas as pd
import random

# Set seed for reproducibility in audits
random.seed(42)

def generate_booking_data(num_records=1000):
    """
    Generates mock booking logs with hidden algorithmic bias 
    for AI Governance auditing purposes.
    """
    data = []
    devices = ['Windows', 'Android', 'Mac', 'iPhone']
    
    for i in range(num_records):
        user_id = f"U_{10000+i}"
        device = random.choice(devices)
        
        # Simulate base hotel price (100 - 500 EUR)
        base_price = random.randint(100, 500)
        
        # BIAS LOGIC (The "Audit Target"): 
        # AI overcharges premium device users by 15% (Proxy Discrimination)
        if device in ['Mac', 'iPhone']:
            final_price = base_price * 1.05
        else:
            final_price = base_price
            
        # AI Confidence Score (0.5 - 0.99)
        confidence = round(random.uniform(0.5, 0.99), 2)
        
        data.append([user_id, device, base_price, round(final_price, 2), confidence])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['user_id', 'device_type', 'base_price', 'final_price', 'ai_confidence'])
    
    # Save to CSV - This will be the source for our SQL Audit tomorrow
    df.to_csv('booking_logs_mock.csv', index=False)
    print(f"Success: {num_records} records generated in 'booking_logs_mock.csv'.")

if __name__ == "__main__":
    generate_booking_data()