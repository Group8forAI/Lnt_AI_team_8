import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
EXCEL_FILE = "Indian_Major_Carps_Dataset.xlsx"
FORECAST_STEPS = 10
TIMESTAMP_COL = "Timestamp"
TANK_COL = "Tank_ID"
OUTPUT_DIR = Path("forecast_plots")
CSV_OUT = "fish_tank_forecasts.csv"

FEATURES_TO_FORECAST = [
    "Temperature_C",
    "Dissolved_Oxygen_mgL",
    "Turbidity_NTU",
    "Water_Quality_Index",
    "Soil_Moisture"
]

OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# LOAD & PREPROCESS DATA
# -----------------------------
df = pd.read_excel(EXCEL_FILE)

# Parse timestamp with day-first format
df[TIMESTAMP_COL] = pd.to_datetime(
    df[TIMESTAMP_COL],
    format="%d-%m-%Y %H:%M",
    errors="raise"
)

# Sort
df = df.sort_values(by=TIMESTAMP_COL)

print(f"\n• Data covers: {df[TIMESTAMP_COL].min()} → {df[TIMESTAMP_COL].max()}")
print(f"• Forecasted features: {', '.join(FEATURES_TO_FORECAST)}")

# -----------------------------
# FORECASTING LOOP
# -----------------------------
all_forecasts = []

# Store model and data for user input predictions
models = {}  # key: (tank_id, feature)

for tank_id, group in df.groupby(TANK_COL):
    group = group.set_index(TIMESTAMP_COL)

    for feature in FEATURES_TO_FORECAST:
        if feature not in group.columns:
            print(f"❌ Feature '{feature}' not found. Skipping.")
            continue

        series = group[feature].dropna()

        if len(series) < 20:
            print(f"⚠  Too few data points for {feature} in tank {tank_id}. Skipping.")
            continue

        try:
            model = ARIMA(series, order=(1, 1, 1))
            model_fit = model.fit()

            # Save model
            models[(tank_id, feature)] = (series, model_fit)

            # Forecast
            inferred_freq = pd.infer_freq(series.index[:20]) or "30T"
            forecast = model_fit.forecast(steps=FORECAST_STEPS)
            forecast_index = pd.date_range(start=series.index[-1], periods=FORECAST_STEPS + 1, freq=inferred_freq)[1:]

            for i in range(FORECAST_STEPS):
                all_forecasts.append({
                    "Tank_ID": tank_id,
                    "Feature": feature,
                    "Forecast_Time": forecast_index[i],
                    "Forecast_Value": forecast.iloc[i]
                })

            # Plot
            plt.figure(figsize=(10, 5))
            plt.plot(series.index, series.values, label="Observed")
            plt.plot(forecast_index, forecast.values, "r--o", label="Forecast")
            plt.title(f"{feature} – Tank {tank_id} (ARIMA(1,1,1))")
            plt.xlabel("Timestamp")
            plt.ylabel(feature)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            filename = f"{feature}_Tank{tank_id}.png".replace(" ", "")
            plt.savefig(OUTPUT_DIR / filename)
            plt.close()
            print(f"✅ Saved plot: {filename}")

        except Exception as e:
            print(f"❌ Error with {feature} in tank {tank_id}: {e}")

# -----------------------------
# SAVE FORECASTS TO CSV
# -----------------------------
forecast_df = pd.DataFrame(all_forecasts)
forecast_df.to_csv(CSV_OUT, index=False)
print(f"\n📄 All forecasts saved to: {CSV_OUT}")

# -----------------------------
# USER INPUT PREDICTION SECTION
# -----------------------------
def predict_at(series, model_fit, ts_point):
    last_time = series.index[-1]
    step = pd.infer_freq(series.index[:10]) or "30T"
    step = pd.Timedelta(step)

    if ts_point <= last_time:
        # Past timestamp – get closest available data
        try:
            return series.asof(ts_point)
        except Exception:
            return np.nan
    else:
        delta_steps = int(np.ceil((ts_point - last_time) / step))
        if delta_steps <= 0:
            return series.iloc[-1]
        forecast = model_fit.forecast(steps=delta_steps)
        return forecast.iloc[-1]

# Ask user for time
try:
    user_input = input("\nEnter ANY timestamp (DD-MM-YYYY HH:MM) ➜ ")
    user_time = datetime.strptime(user_input, "%d-%m-%Y %H:%M")
except Exception:
    print("❌ Invalid format. Use DD-MM-YYYY HH:MM")
    exit()

# Generate other target times
now = datetime.now().replace(second=0, microsecond=0)
future_times = {
    "User time": user_time,
    "Now + 30 min": now + timedelta(minutes=30),
    "Tomorrow same time": now + timedelta(days=1),
    "Next month same time": now + pd.DateOffset(months=1)
}

for tank_id in df[TANK_COL].unique():
    for label, target_time in future_times.items():
        print(f"\nTank {tank_id} | {label} ({target_time.strftime('%d-%m-%Y %H:%M')})")
        for feature in FEATURES_TO_FORECAST:
            key = (tank_id, feature)
            if key not in models:
                print(f"  {feature}: [No model]")
                continue

            series, model_fit = models[key]
            val = predict_at(series, model_fit, pd.Timestamp(target_time))
            print(f"  {feature}: {val:.2f}")