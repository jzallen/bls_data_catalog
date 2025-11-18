#!/usr/bin/env python3
"""
Generate sample BLS-like employment and unemployment data for demonstration.
This creates realistic-looking time series data for all 50 states.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set seed for reproducibility
random.seed(42)

# State FIPS codes
STATE_FIPS = [
    '01', '02', '04', '05', '06', '08', '09', '10', '11', '12',
    '13', '15', '16', '17', '18', '19', '20', '21', '22', '23',
    '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
    '34', '35', '36', '37', '38', '39', '40', '41', '42', '44',
    '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56'
]

# Base employment levels (in thousands) for different sized states
STATE_BASE_EMPLOYMENT = {
    '06': 17000,  # California - largest
    '48': 13000,  # Texas
    '36': 9000,   # New York
    '12': 9000,   # Florida
    '17': 6000,   # Illinois
    '42': 6000,   # Pennsylvania
    '39': 5500,   # Ohio
    '13': 4500,   # Georgia
    '37': 4500,   # North Carolina
    '26': 4300,   # Michigan
}

# Assign reasonable employment levels to remaining states
for fips in STATE_FIPS:
    if fips not in STATE_BASE_EMPLOYMENT:
        # Smaller states get employment between 500k and 3000k
        STATE_BASE_EMPLOYMENT[fips] = random.randint(500, 3000)

def generate_monthly_dates(start_year=2022, start_month=1, num_months=36):
    """Generate monthly date strings"""
    dates = []
    current = datetime(start_year, start_month, 1)
    for _ in range(num_months):
        dates.append(current.strftime('%Y-%m-%d'))
        # Move to next month
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)
    return dates

def generate_employment_data():
    """Generate employment level data with realistic trends"""
    dates = generate_monthly_dates()
    
    data = []
    for state_fips in STATE_FIPS:
        base_employment = STATE_BASE_EMPLOYMENT[state_fips]
        
        # Add trend: general growth with some volatility
        trend = 0
        for date in dates:
            # Monthly growth rate (annualized 2% growth = ~0.165% monthly)
            monthly_growth = random.gauss(0.0015, 0.003)
            trend += monthly_growth
            
            employment = int(base_employment * (1 + trend))
            
            data.append({
                'state_fips': state_fips,
                'year_month': date,
                'employment_level': employment,
                'series_id': f'LAUST{state_fips}0000000000003'
            })
    
    return data

def generate_unemployment_data():
    """Generate unemployment rate data with realistic patterns"""
    dates = generate_monthly_dates()
    
    data = []
    for state_fips in STATE_FIPS:
        # Base unemployment rate between 2.5% and 6.5%
        base_rate = random.uniform(2.5, 6.5)
        
        # Add seasonal and random variation
        for i, date in enumerate(dates):
            # Seasonal component (higher in winter)
            month = datetime.strptime(date, '%Y-%m-%d').month
            seasonal = 0.3 * (1 if month in [1, 2, 12] else -0.2 if month in [6, 7, 8] else 0)
            
            # Random walk
            noise = random.gauss(0, 0.15)
            
            # Slight downward trend over time
            trend = -0.02 * (i / len(dates))
            
            rate = max(2.0, min(12.0, base_rate + seasonal + noise + trend))
            
            labor_force = int(STATE_BASE_EMPLOYMENT[state_fips] * random.uniform(1.02, 1.05))
            unemployed = int(labor_force * rate / 100)
            
            data.append({
                'state_fips': state_fips,
                'year_month': date,
                'unemployment_rate': round(rate, 1),
                'labor_force': labor_force,
                'unemployed': unemployed,
                'series_id': f'LAUST{state_fips}0000000000004'
            })
    
    return data

def main():
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Generate employment data
    print("Generating employment data...")
    employment_data = generate_employment_data()
    employment_file = data_dir / 'employment_monthly.csv'
    
    with open(employment_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['state_fips', 'year_month', 'employment_level', 'series_id'])
        writer.writeheader()
        writer.writerows(employment_data)
    
    print(f"  ✓ Created {employment_file} with {len(employment_data)} rows")
    
    # Generate unemployment data
    print("Generating unemployment data...")
    unemployment_data = generate_unemployment_data()
    unemployment_file = data_dir / 'unemployment_monthly.csv'
    
    with open(unemployment_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['state_fips', 'year_month', 'unemployment_rate', 'labor_force', 'unemployed', 'series_id'])
        writer.writeheader()
        writer.writerows(unemployment_data)
    
    print(f"  ✓ Created {unemployment_file} with {len(unemployment_data)} rows")
    print("\nDone! Run 'dbt seed' to load data into DuckDB.")

if __name__ == '__main__':
    main()
