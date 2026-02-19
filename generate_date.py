from faker import Faker
import pandas as pd
import random as rn
import numpy as np
fake = Faker("en_GB") # Create a Faker instance (en_GB creates UK-style company names)

# This code generates two datasets: a financial fact table, and a client dimension table. The financial fact table contains 1000 rows, while the client dimension table contains 100 rows. The financial fact table includes a foreign key that references the client dimension table.


### CLIENT DATAFRAME: 500 clients, one row per client
# Fields: ID, Name, Industry, Address, Region, Tier, Size, Since Date, Relationship Manager

# Possible values for industry, region, tier and size
# Weights determine randomisation frequency
industries = ["Banking", "Energy", "Tech", "Healthcare", "Private Equity", "Retail", "Manufacturing", "Transport", "Media", "Education"]
industry_weights = [15, 10, 15, 8, 5, 10, 8, 7, 3, 1] 

regions = ["London", "South East", "North West", "Scotland", "Wales","Other"]
region_weights = [30, 20, 15, 10, 5, 20] 

tiers = ["A+","A", "B", "C"]
tier_weights = [5, 15, 30, 50]
company_sizes = ["<50", "50-250", "250-1000", "1000+"]
size_weights = [20, 30, 30, 20]

client_data = pd.DataFrame({
    "client_id": i+1,
    "client_name": fake.company(),
    "region": np.random.choice(regions, p=region_weights),
    "industry": np.random.choice(industries, p=industry_weights),
    "tier": np.random.choice(tiers, p=tier_weights),
    "size": np.random.choice(company_sizes, p=size_weights),
    "since_date": fake.date_between(start_date='-12y', end_date='today')
    # assumes clients never leave for convenience
}

