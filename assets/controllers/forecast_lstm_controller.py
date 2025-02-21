import pandas as pd
from fastapi import HTTPException
from modelos import get_model_prediction
from assets.models.forecast_lstm_model import ForecastRequest

async def generate_forecast(request: ForecastRequest):
    """Generate forecast using pre-trained LSTM model"""
    try:
        # Convert input data to pandas Series
        dates = pd.to_datetime(request.data.dates)
        values = request.data.values
        df = pd.DataFrame({'Close': values}, index=dates)
        
        # Get predictions and plot from pre-trained model
        predictions, plot_base64 = get_model_prediction(
            request.ticker,  # Add ticker to ForecastRequest
            df,
            return_plot=True  # Request plot generation
        )
        
        # Create future dates for predictions
        last_date = dates[-1]
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=len(predictions),
            freq='B'
        )
        
        # Format response
        forecast_dates = future_dates.strftime('%Y-%m-%d').tolist()
        forecast_values = predictions.tolist()
        
        return {
            "forecast_dates": forecast_dates,
            "forecast_values": forecast_values,
            "plot_base64": plot_base64
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 