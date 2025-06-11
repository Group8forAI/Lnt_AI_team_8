import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


def generate_indian_carp_dataset():
    """
    Generate comprehensive fish hatchery dataset for Indian Major Carps
    Based on specific requirements for Rohu, Catla, and Mrigal
    6000 rows total: 2000 rows per tank
    """

    # Indian Major Carps Optimal Thresholds
    THRESHOLDS = {
        'temperature': {'optimal': (26, 30), 'acceptable': (24, 32), 'critical': (22, 35)},
        'dissolved_oxygen': {'optimal': (5, 8), 'acceptable': (4, 9), 'critical': (3, 12)},
        'ph': {'optimal': (7.0, 8.5), 'acceptable': (6.5, 9.0), 'critical': (6.0, 9.5)},
        'ammonia': {'optimal': (0, 0.1), 'acceptable': (0, 0.5), 'critical': (0, 1.0)},
        'nitrate': {'optimal': (0, 10), 'acceptable': (0, 25), 'critical': (0, 40)},
        'turbidity': {'optimal': (15, 40), 'acceptable': (10, 60), 'critical': (5, 80)},
        'alkalinity': {'optimal': (80, 120), 'acceptable': (60, 150), 'critical': (40, 200)},
        'hardness': {'optimal': (75, 150), 'acceptable': (50, 200), 'critical': (30, 250)}
    }

    # Carp species characteristics
    CARP_SPECIES = {
        1: 'Rohu',  # Surface and column feeder
        2: 'Catla',  # Surface feeder
        3: 'Mrigal'  # Bottom feeder
    }

    # Generate timestamps (every 2 minutes for comprehensive coverage)
    start_time = datetime(2025, 6, 1, 0, 0, 0)
    timestamps = []
    for i in range(3000):
        timestamps.append(start_time + timedelta(minutes=i * 30))

    dataset = []
    entry_id = 1

    for timestamp in timestamps:
        for tank_id in [1, 2, 3]:  # Tank 1=Rohu, Tank 2=Catla, Tank 3=Mrigal

            # Species-specific parameter generation
            species = CARP_SPECIES[tank_id]

            # Base parameters with species-specific adjustments
            if species == 'Rohu':
                # Rohu prefers slightly warmer water, moderate DO
                temperature_base = 28.0
                do_base = 6.5
                ph_base = 7.8
                turbidity_base = 25
            elif species == 'Catla':
                # Catla prefers surface feeding, higher DO
                temperature_base = 27.5
                do_base = 7.0
                ph_base = 7.5
                turbidity_base = 30
            else:  # Mrigal
                # Mrigal is bottom feeder, tolerates higher turbidity
                temperature_base = 27.0
                do_base = 6.0
                ph_base = 7.3
                turbidity_base = 35

            # Generate parameters with realistic variations
            temperature = np.random.normal(temperature_base, 1.5)
            temperature = max(22, min(35, temperature))

            dissolved_oxygen = np.random.normal(do_base, 1.2)
            dissolved_oxygen = max(3, min(12, dissolved_oxygen))

            ph = np.random.normal(ph_base, 0.4)
            ph = max(6.0, min(9.5, ph))

            ammonia = np.random.exponential(0.12)
            ammonia = min(1.0, ammonia)

            nitrate = np.random.exponential(6)
            nitrate = min(40, nitrate)

            turbidity = np.random.normal(turbidity_base, 8)
            turbidity = max(5, min(80, turbidity))

            alkalinity = np.random.normal(100, 20)
            alkalinity = max(40, min(200, alkalinity))

            hardness = np.random.normal(110, 25)
            hardness = max(30, min(250, hardness))

            soil_moisture = np.random.normal(3800, 120)
            soil_moisture = max(3500, min(4100, soil_moisture))

            # Water flow rate (L/min)
            water_flow = np.random.normal(150, 25)
            water_flow = max(100, min(200, water_flow))

            # Feeding frequency (times per day)
            feeding_freq = random.choice([2, 3, 4])

            # Classification Labels Generation

            # 1. Tank Leakage (0 or 1)
            if soil_moisture > 4000 or (soil_moisture > 3950 and np.random.random() < 0.25):
                tank_leakage = 1
                soil_moisture = np.random.uniform(4000, 4100)
            else:
                tank_leakage = 0

            # 2. Temperature Status
            if THRESHOLDS['temperature']['optimal'][0] <= temperature <= THRESHOLDS['temperature']['optimal'][1]:
                temp_status = "Optimal"
            elif THRESHOLDS['temperature']['acceptable'][0] <= temperature <= THRESHOLDS['temperature']['acceptable'][
                1]:
                temp_status = "Acceptable"
            else:
                temp_status = "Critical"

            # 3. Water Quality Index (based on multiple parameters)
            quality_score = 0

            # Temperature score
            if THRESHOLDS['temperature']['optimal'][0] <= temperature <= THRESHOLDS['temperature']['optimal'][1]:
                quality_score += 4
            elif THRESHOLDS['temperature']['acceptable'][0] <= temperature <= THRESHOLDS['temperature']['acceptable'][
                1]:
                quality_score += 2

            # DO score
            if THRESHOLDS['dissolved_oxygen']['optimal'][0] <= dissolved_oxygen <= \
                    THRESHOLDS['dissolved_oxygen']['optimal'][1]:
                quality_score += 4
            elif THRESHOLDS['dissolved_oxygen']['acceptable'][0] <= dissolved_oxygen <= \
                    THRESHOLDS['dissolved_oxygen']['acceptable'][1]:
                quality_score += 2

            # pH score
            if THRESHOLDS['ph']['optimal'][0] <= ph <= THRESHOLDS['ph']['optimal'][1]:
                quality_score += 3
            elif THRESHOLDS['ph']['acceptable'][0] <= ph <= THRESHOLDS['ph']['acceptable'][1]:
                quality_score += 1

            # Ammonia score
            if ammonia <= THRESHOLDS['ammonia']['optimal'][1]:
                quality_score += 3
            elif ammonia <= THRESHOLDS['ammonia']['acceptable'][1]:
                quality_score += 1

            # Nitrate score
            if nitrate <= THRESHOLDS['nitrate']['optimal'][1]:
                quality_score += 2
            elif nitrate <= THRESHOLDS['nitrate']['acceptable'][1]:
                quality_score += 1

            if quality_score >= 14:
                water_quality = "Excellent"
            elif quality_score >= 10:
                water_quality = "Good"
            elif quality_score >= 6:
                water_quality = "Fair"
            else:
                water_quality = "Poor"

            # 4. DO Status
            if THRESHOLDS['dissolved_oxygen']['optimal'][0] <= dissolved_oxygen <= \
                    THRESHOLDS['dissolved_oxygen']['optimal'][1]:
                do_status = "Optimal"
            elif THRESHOLDS['dissolved_oxygen']['acceptable'][0] <= dissolved_oxygen <= \
                    THRESHOLDS['dissolved_oxygen']['acceptable'][1]:
                do_status = "Acceptable"
            else:
                do_status = "Critical"

            # 5. Growth Condition (based on overall parameters)
            growth_factors = 0

            if temp_status == "Optimal":
                growth_factors += 3
            elif temp_status == "Acceptable":
                growth_factors += 1

            if do_status == "Optimal":
                growth_factors += 3
            elif do_status == "Acceptable":
                growth_factors += 1

            if water_quality in ["Excellent", "Good"]:
                growth_factors += 2
            elif water_quality == "Fair":
                growth_factors += 1

            if THRESHOLDS['turbidity']['optimal'][0] <= turbidity <= THRESHOLDS['turbidity']['optimal'][1]:
                growth_factors += 1

            if growth_factors >= 8:
                growth_condition = "Excellent"
            elif growth_factors >= 6:
                growth_condition = "Good"
            elif growth_factors >= 4:
                growth_condition = "Fair"
            else:
                growth_condition = "Poor"

            # Round values
            temperature = round(temperature, 1)
            dissolved_oxygen = round(dissolved_oxygen, 1)
            ph = round(ph, 1)
            ammonia = round(ammonia, 3)
            nitrate = round(nitrate, 1)
            turbidity = round(turbidity, 1)
            alkalinity = round(alkalinity, 1)
            hardness = round(hardness, 1)
            soil_moisture = int(soil_moisture)
            water_flow = round(water_flow, 1)

            # Create row
            row = {
                'Timestamp': timestamp.strftime('%d-%m-%Y %H:%M'),
                'Entry_ID': entry_id,
                'Tank_ID': tank_id,
                'Carp_Species': species,
                'Temperature_C': temperature,
                'Dissolved_Oxygen_mgL': dissolved_oxygen,
                'pH': ph,
                'Ammonia_mgL': ammonia,
                'Nitrate_mgL': nitrate,
                'Turbidity_NTU': turbidity,
                'Alkalinity_mgL': alkalinity,
                'Hardness_mgL': hardness,
                'Soil_Moisture': soil_moisture,
                'Water_Flow_Lmin': water_flow,
                'Feeding_Frequency': feeding_freq,
                'Tank_Leakage': tank_leakage,
                'Temperature_Status': temp_status,
                'Water_Quality_Index': water_quality,
                'DO_Status': do_status,
                'Growth_Condition': growth_condition
            }

            dataset.append(row)
            entry_id += 1

    return pd.DataFrame(dataset)


# Generate the dataset
print("Generating Indian Major Carps Dataset...")
df = generate_indian_carp_dataset()


# Create separate sheets for thresholds and main data
def create_threshold_sheet():
    """Create a threshold reference sheet"""
    threshold_data = []

    parameters = [
        ('Temperature (°C)', 'Optimal: 26-30°C, Acceptable: 24-32°C, Critical: <24 or >32°C'),
        ('Dissolved Oxygen (mg/L)', 'Optimal: 5-8 mg/L, Acceptable: 4-9 mg/L, Critical: <4 or >9 mg/L'),
        ('pH', 'Optimal: 7.0-8.5, Acceptable: 6.5-9.0, Critical: <6.5 or >9.0'),
        ('Ammonia (mg/L)', 'Optimal: 0-0.1 mg/L, Acceptable: 0-0.5 mg/L, Critical: >0.5 mg/L'),
        ('Nitrate (mg/L)', 'Optimal: 0-10 mg/L, Acceptable: 0-25 mg/L, Critical: >25 mg/L'),
        ('Turbidity (NTU)', 'Optimal: 15-40 NTU, Acceptable: 10-60 NTU, Critical: <10 or >60 NTU'),
        ('Alkalinity (mg/L)', 'Optimal: 80-120 mg/L, Acceptable: 60-150 mg/L, Critical: <60 or >150 mg/L'),
        ('Hardness (mg/L)', 'Optimal: 75-150 mg/L, Acceptable: 50-200 mg/L, Critical: <50 or >200 mg/L')
    ]

    for param, range_desc in parameters:
        threshold_data.append({
            'Parameter': param,
            'Threshold_Ranges': range_desc,
            'Species_Notes': 'Applicable to Rohu, Catla, and Mrigal with minor species-specific variations'
        })

    return pd.DataFrame(threshold_data)


# Create species information sheet
def create_species_info():
    species_data = [
        {
            'Tank_ID': 1,
            'Species': 'Rohu (Labeo rohita)',
            'Feeding_Habit': 'Column feeder',
            'Preferred_Temperature': '27-29°C',
            'Growth_Rate': 'Fast',
            'Special_Requirements': 'Prefers slightly higher temperature, good water circulation'
        },
        {
            'Tank_ID': 2,
            'Species': 'Catla (Catla catla)',
            'Feeding_Habit': 'Surface feeder',
            'Preferred_Temperature': '26-28°C',
            'Growth_Rate': 'Very Fast',
            'Special_Requirements': 'Requires high dissolved oxygen, surface feeding space'
        },
        {
            'Tank_ID': 3,
            'Species': 'Mrigal (Cirrhinus mrigala)',
            'Feeding_Habit': 'Bottom feeder',
            'Preferred_Temperature': '25-28°C',
            'Growth_Rate': 'Moderate',
            'Special_Requirements': 'Tolerates higher turbidity, bottom substrate important'
        }
    ]
    return pd.DataFrame(species_data)


# Generate additional sheets
threshold_df = create_threshold_sheet()
species_df = create_species_info()

# Display information
print(f"\nDataset Shape: {df.shape}")
print(f"Total Rows: {len(df)}")
print("\nSpecies Distribution:")
print(df['Carp_Species'].value_counts())

print("\nClassification Distributions:")
print("\n1. Tank Leakage:", df['Tank_Leakage'].value_counts().to_dict())
print("2. Temperature Status:", df['Temperature_Status'].value_counts().to_dict())
print("3. Water Quality Index:", df['Water_Quality_Index'].value_counts().to_dict())
print("4. DO Status:", df['DO_Status'].value_counts().to_dict())
print("5. Growth Condition:", df['Growth_Condition'].value_counts().to_dict())

# Save to Excel with multiple sheets
with pd.ExcelWriter('Indian_Major_Carps_Dataset.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Main_Dataset', index=False)
    threshold_df.to_excel(writer, sheet_name='Parameter_Thresholds', index=False)
    species_df.to_excel(writer, sheet_name='Species_Information', index=False)

print("\n✅ Excel file saved as 'Indian_Major_Carps_Dataset.xlsx'")
print("📊 Contains 3 sheets:")
print("   - Main_Dataset: Complete 6000-row dataset")
print("   - Parameter_Thresholds: Optimal ranges for each parameter")
print("   - Species_Information: Details about each carp species")

# Show sample data
print("\n=== SAMPLE DATA ===")
sample_data = df.head(9)  # 3 rows per species
print(sample_data[['Timestamp', 'Tank_ID', 'Carp_Species', 'Temperature_C', 'Dissolved_Oxygen_mgL',
                   'pH', 'Growth_Condition', 'Water_Quality_Index']].to_string(index=False))

print("\n=== PARAMETER STATISTICS ===")
numeric_cols = ['Temperature_C', 'Dissolved_Oxygen_mgL', 'pH', 'Ammonia_mgL', 'Nitrate_mgL', 'Turbidity_NTU']
print(df[numeric_cols].describe())