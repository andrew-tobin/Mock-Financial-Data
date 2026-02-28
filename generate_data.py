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
industry_weights = [0.2, 0.15, 0.15, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05]

regions = ["London", "South East", "North West", "Scotland", "Wales","Other"]
region_weights = [0.4, 0.2, 0.15, 0.1, 0.05, 0.1] 

tiers = ["A+","A", "B", "C"]
tier_weights = [0.1, 0.3, 0.4, 0.2]
company_sizes = ["<50", "50-250", "250-1000", "1000+"]
size_weights = [0.25, 0.35, 0.25, 0.15]

client_data = pd.DataFrame({
    "client_id": i,
    "client_name": fake.company(),
    "region": np.random.choice(regions, p=region_weights),
    "industry": np.random.choice(industries, p=industry_weights),
    "tier": np.random.choice(tiers, p=tier_weights),
    "size": np.random.choice(company_sizes, p=size_weights),
    "start_date": fake.date_between(start_date='-12y', end_date='today'),
    "end_date": None 
    } for i in range(500))

# Set end_date for some clients (doing after df creation to ensure end_date is after start_date)
for i in range(len(client_data)):
    if rn.random() < 0.3:  # 30% of clients have ended relationship
        client_data.at[i, "end_date"] = fake.date_between(start_date=client_data.at[i, "start_date"], end_date='today')

### FINANCIAL DATAFRAME: same clients as above, 8 years of data (one row per client per year)
# Fields: Client ID, Year, Revenue, RWA

# Adding to list in nested for loops then converting to dataframe after

financial_data = []
for client_id in client_data["client_id"]:
    tier_multiplier = {"A+": 5, "A": 3, "B": 1.0, "C": 0.5}[client_data.at[client_id, "tier"]]
    this_year_rwa = tier_multiplier * round(rn.randint(100000, 50000000))  # Starting RWA for the client
    this_year_revenue = tier_multiplier*round(this_year_rwa * rn.uniform(0.0, 0.2))  # Revenue is a function of RWA and a random RORWA
    for year in range(2018, 2026):  # 8 years of data
        # Only generate for years client has been with the bank
        if client_data.at[client_id, "start_date"].year > year and (client_data.at[client_id, "end_date"] is None or client_data.at[client_id, "end_date"].year < year):
                
            financial_data.append({
                "client_id": client_id,
                "year": year,
                # Allow for random IB revenue spikes without persisting next year
                # e.g. from m&a fees
                "revenue":round(this_year_revenue * rn.uniform(1.5, 5.0))
                if rn.random() < 0.05
                else this_year_revenue,
                "rwa": round(rn.uniform(1e6, 1e9), 2),    
                "rorwa": round(rn.uniform(0.01, 0.2), 4)  
            })
        # Change RWA and revenue +/-10% and +/-20% for next year
        this_year_rwa *= rn.uniform(0.9, 1.1)  
        this_year_revenue *= rn.uniform(0.8, 1.2)  

financial_df = pd.DataFrame(financial_data)



### SAVE DATAFRAMES TO CSV
client_data.to_csv("client_dimension.csv", index=False)
financial_df.to_csv("financial_fact.csv", index=False)