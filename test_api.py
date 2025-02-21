import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import matplotlib
# Set the backend to 'Agg' before importing pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
from pytz import timezone
from assets.controllers.forecast_var_controller import fetch_data
from modelos.SARIMA import SARIMAModel

def get_stock_data(days=100, ticker='VALE3.SA', delay_days=0):
    """
    Get historical stock data for the specified ticker and time period
    If delay_days is specified, it will get data up to that many days ago
    """
    try:
        # Add delay_days to the requested period to ensure we have enough historical data
        total_days = days + delay_days
        df = fetch_data(["BRL=X", "PETR4.SA", "VALE3.SA", "WEGE3.SA", "GLD"], period=f"{total_days}d")
        
        # Get the Close price for the specified ticker
        data = df[('Close', ticker)]
        
        if delay_days > 0:
            # Split the data into training and validation sets
            training_data = data[:-delay_days]
            validation_data = data[-delay_days:]
            print(f"Successfully fetched {len(training_data)} days of {ticker} training data")
            print(f"Validation data available: {len(validation_data)} days")
            
            return {
                "training": {
                    "dates": training_data.index.strftime('%Y-%m-%d').tolist(),
                    "values": training_data.values.tolist()
                },
                "validation": {
                    "dates": validation_data.index.strftime('%Y-%m-%d').tolist(),
                    "values": validation_data.values.tolist()
                }
            }
        else:
            print(f"Successfully fetched {len(data)} days of {ticker} price data")
            return {
                "dates": data.index.strftime('%Y-%m-%d').tolist(),
                "values": data.values.tolist()
            }
        
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        return None

def test_forecast_endpoint(validation_days=5):
    """Test the forecast endpoint with stock price data and validate predictions"""
    url = "http://localhost:8000/forecast_sarima/"
    
    # Get data with validation period
    data = get_stock_data(days=365, ticker='VALE3.SA', delay_days=validation_days)
    
    if not data:
        print("Failed to fetch stock price data")
        return None
    
    # Prepare request payload using only training data
    payload = {
        "data": data["training"],
        "n_steps": validation_days,  # Forecast the validation period
        "order": [2, 1, 2],
        "seasonal_order": [1, 1, 1, 5]
    }
    
    try:
        # Send POST request to the API
        response = requests.post(url, json=payload)
        response.raise_for_status()
        forecast = response.json()
        
        # Print results and comparison
        print("\nForecast vs Actual Results:")
        print("==========================")
        print("Date            Forecast    Actual      Diff    Diff%")
        print("----------------------------------------------------")
        
        for date, pred, actual in zip(
            forecast["forecast_dates"],
            forecast["forecast_values"],
            data["validation"]["values"]
        ):
            diff = actual - pred
            diff_pct = (diff / actual) * 100
            print(f"{date}  R${pred:8.2f}  R${actual:8.2f}  {diff:8.2f}  {diff_pct:6.2f}%")
            
        # Calculate error metrics
        predictions = np.array(forecast["forecast_values"])
        actuals = np.array(data["validation"]["values"])
        mse = np.mean((predictions - actuals) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - actuals))
        mape = np.mean(np.abs((predictions - actuals) / actuals)) * 100
        
        print("\nError Metrics:")
        print(f"MSE:  {mse:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE:  {mae:.4f}")
        print(f"MAPE: {mape:.2f}%")
        
        return {
            "forecast": forecast,
            "validation": data["validation"],
            "metrics": {
                "mse": mse,
                "rmse": rmse,
                "mae": mae,
                "mape": mape
            }
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
        return None

def test_health_endpoint():
    """Test the health check endpoint"""
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("\nHealth Check:")
        print("=============")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking health: {str(e)}")
        return None

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Test health endpoint
    health_status = test_health_endpoint()
    
    # Test forecast endpoint
    if health_status and health_status.get("status") == 'ok':
        results = test_forecast_endpoint(validation_days=5)
        
        if results:
            # Create visualization with training, validation, and forecast data
            historical_data = get_stock_data(ticker='VALE3.SA')
            
            plt.figure(figsize=(15, 8))
            
            # Plot historical data
            plt.plot(historical_data["dates"], 
                    historical_data["values"], 
                    label='Historical Price',
                    color='blue',
                    alpha=0.6)
            
            # Plot validation data
            plt.plot(results["validation"]["dates"],
                    results["validation"]["values"],
                    label='Actual Values',
                    color='green',
                    marker='o')
            
            # Plot forecast
            plt.plot(results["forecast"]["forecast_dates"], 
                    results["forecast"]["forecast_values"], 
                    label='Forecast',
                    color='red',
                    linestyle='--',
                    marker='o')
            
            plt.title(f"Vale Stock Price Forecast vs Actual (MAPE: {results['metrics']['mape']:.2f}%)")
            plt.xlabel("Date")
            plt.ylabel("Price (BRL)")
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            
            # Save plot to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"vale3_forecast_validation_{timestamp}.png")
            plt.savefig(filename)
            plt.close()
            
            print(f"\nPlot saved to: {filename}") 