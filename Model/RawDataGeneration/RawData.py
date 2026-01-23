
import pandas as pd  # Data manipulation
import numpy as np   # Numerical operations
import os            # File paths
import random        # Random generation
from faker import Faker  # Realistic fake data
from datetime import datetime, timedelta # Time handling

# Initialize Faker
faker = Faker()

# ==========================================
# CONFIGURATION
# ==========================================
NUM_ROWS = 100000
OUTPUT_FILE = "RawDataset.csv"
NUM_USERS = 5000
START_DATE = datetime(2025, 1, 1) # Simulation start date
DAYS_RANGE = 90 # Generates data for 3 months

# ==========================================
# 1. INITIALIZE LISTS
# ==========================================
user_ids = [] # Description: Unique identifier for each user.
roles = [] # Description: Job role (Admin, Employee, Vendor, etc.).
timestamps = [] # Unit: Datetime | Description: Exact date and time of the login event.
login_hours = [] # Unit: Hour (0-23) | Description: The hour of the day the session started (e.g., 14 = 2 PM).
session_durations = [] # Unit: Minutes | Description: Total time spent in the session.
data_download_mbs = [] # Unit: MB | Description: Total data downloaded during the session.
transaction_amounts = [] # Unit: USD | Description: Total value of transactions performed.
access_counts = [] # Unit: Count | Description: Number of resources/files accessed.
privilege_levels = [] # Unit: Level (1-5) | Description: Security clearance level used in session.
device_changes = [] # Unit: Binary (0/1) | Description: 1 if the device used is different from usual.
location_changes = [] # Unit: Binary (0/1) | Description: 1 if the location (IP/Geo) is different from usual.
failed_logins_list = [] # Unit: Count | Description: Number of failed password attempts before success.
is_off_hours_list = [] # Unit: Binary (0/1) | Description: 1 if login is outside standard working hours (8 PM - 7 AM).
login_frequencies = [] # Unit: Count/Day | Description: How many times the user logged in today.
attack_types = [] # Description: Label for the scenario (Normal, Brute Force, Exfiltration, etc.).
risk_scores = [] # Unit: Probability (0-1) | Description: Calculated likelihood of this session being a threat.

# ==========================================
# 2. CREATE CONSISTENT USER POOL
# ==========================================
print("Initializing User Pool...")
pool_user_ids = []
pool_roles = []

role_types = ['Employee', 'Manager', 'Vendor', 'Contractor', 'Admin']
# Risk multipliers for roles
role_weights = [0.6, 0.1, 0.15, 0.1, 0.05] 

for _ in range(NUM_USERS):
    pool_user_ids.append(faker.uuid4()[:8])
    pool_roles.append(np.random.choice(role_types, p=role_weights))

print(f"Generating {NUM_ROWS} rows with enhanced patterns, timestamps, and attack labels...")

# ==========================================
# 3. GENERATE DATA (LINEAR LOOP)
# ==========================================
for i in range(NUM_ROWS):
    
    # --- A. Select User ---
    idx = random.randint(0, NUM_USERS - 1)
    u_id = pool_user_ids[idx]
    role = pool_roles[idx]
    
    user_ids.append(u_id)
    roles.append(role)
    
    # --- B. Determine Scenario ---
    # 0: Normal (80%)
    # 1: Data Exfiltration (5%)
    # 2: Brute Force (5%)
    # 3: Privilege Abuse (5%)
    # 4: Account Sharing / Anomalous Travel (5%)
    scenario = np.random.choice([0, 1, 2, 3, 4], p=[0.80, 0.05, 0.05, 0.05, 0.05])
    
    # Defaults (Normal Behavior)
    l_hour = np.random.choice(range(8, 19)) # Normal work hours
    duration = int(np.random.normal(45, 15)) 
    download = int(np.random.exponential(10)) 
    amount = int(np.random.exponential(500)) 
    access = int(np.random.poisson(5))
    privilege = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.3, 0.1, 0.05, 0.05])
    dev_change = 0 
    loc_change = 0
    fails = 0
    freq = np.random.randint(1, 5)
    attack_label = 'Normal'

    # --- C. Apply Scenario Logic ---
    
    if scenario == 1: # Data Exfiltration
        attack_label = 'Data Exfiltration'
        l_hour = np.random.choice([22, 23, 0, 1, 2, 3, 4]) # Off hours
        download = int(np.random.normal(2500, 800)) 
        duration = np.random.choice([10, 400]) 
        loc_change = np.random.choice([0, 1], p=[0.3, 0.7]) 
        
    elif scenario == 2: # Brute Force / Automation
        attack_label = 'Brute Force'
        fails = np.random.randint(5, 20) 
        dev_change = 1 
        loc_change = 1 
        l_hour = np.random.choice([1, 2, 3, 4])
        access = int(np.random.poisson(50)) 
        duration = np.random.randint(1, 5) 
        
    elif scenario == 3: # Privilege Abuse
        attack_label = 'Privilege Abuse'
        if role in ['Admin', 'Manager']:
            privilege = 5
            amount = int(np.random.normal(60000, 15000)) 
            download = int(np.random.normal(500, 100)) 
        else:
            privilege = np.random.choice([4, 5]) 
            fails = np.random.randint(2, 5) 
            access = np.random.randint(20, 40) 
            
    elif scenario == 4: # Anomalous Travel / Account Sharing
        attack_label = 'Account Sharing'
        loc_change = 1
        dev_change = 1
        l_hour = np.random.choice(range(8, 20)) 
        access = int(np.random.poisson(10)) 
            
    # Cleanup bounds
    duration = max(1, duration)
    download = max(0, download)
    amount = max(0, amount)

    # --- D. Generate Timestamp ---
    # Random day in range
    random_days = random.randint(0, DAYS_RANGE)
    # Random minute and second
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    # Construct Datetime
    dt = START_DATE + timedelta(days=random_days)
    dt = dt.replace(hour=l_hour, minute=random_minute, second=random_second)
    timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Store Feature Values
    timestamps.append(timestamp_str)
    login_hours.append(l_hour)
    session_durations.append(duration)
    data_download_mbs.append(download)
    transaction_amounts.append(amount)
    access_counts.append(access)
    privilege_levels.append(privilege)
    device_changes.append(dev_change)
    location_changes.append(loc_change)
    failed_logins_list.append(fails)
    login_frequencies.append(freq)
    attack_types.append(attack_label)
    
    # Derived Feature
    is_off_hours = 1 if (l_hour < 7 or l_hour > 20) else 0
    is_off_hours_list.append(is_off_hours)
    
    # ==========================================
    # 4. RISK SCORE CALCULATION
    # ==========================================
    risk = 0.05 # Base
    
    # Role Impact
    if role == 'Admin': risk += 0.15      
    elif role == 'Vendor': risk += 0.15   
    elif role == 'Contractor': risk += 0.10
    
    # Feature Impact
    if is_off_hours: risk += 0.15
    if download > 1000: risk += 0.40 
    elif download > 250: risk += 0.15
    if amount > 20000: risk += 0.35 
    elif amount > 5000: risk += 0.10
    if fails > 5: risk += 0.30
    elif fails > 2: risk += 0.10
    if loc_change and dev_change: risk += 0.20
    elif loc_change: risk += 0.10
    if privilege >= 4 and role not in ['Admin', 'Manager']: risk += 0.25 
    if privilege == 5: risk += 0.10 
    if duration < 3 and access > 10: risk += 0.15 
    if access > 40: risk += 0.10 
    
    # Normalize
    noise = np.random.uniform(-0.03, 0.03)
    final_risk = risk + noise
    if final_risk > 1.0: final_risk = 1.0
    if final_risk < 0.0: final_risk = 0.0
    
    risk_scores.append(round(final_risk, 4))

# ==========================================
# 5. SAVE DATASET
# ==========================================
data = {
    "timestamp": timestamps, # New Column
    "user_id": user_ids,
    "role": roles,
    "login_hour": login_hours,
    "session_duration": session_durations,
    "data_download_mb": data_download_mbs,
    "transaction_amount": transaction_amounts,
    "access_count": access_counts,
    "privilege_level": privilege_levels,
    "device_change": device_changes,
    "location_change": location_changes,
    "failed_logins": failed_logins_list,
    "is_off_hours": is_off_hours_list,
    "login_frequency": login_frequencies,
    "attack_type": attack_types,
    "risk_score": risk_scores
}

df = pd.DataFrame(data)

# Sort by timestamp for realism
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by='timestamp')

print(f"Saving to {OUTPUT_FILE}...")
df.to_csv(OUTPUT_FILE, index=False)
print("Done!")
print("\nSample Data:")
print(df[['timestamp', 'user_id', 'role', 'login_hour', 'attack_type', 'risk_score']].head())
