import pandas as pd
from fastapi import HTTPException
from modelos.SARIMA import SARIMAModel
from assets.models.forecast_sarima_model import ForecastRequest

async def generate_forecast(request: ForecastRequest):
    """Generate forecast using SARIMA model"""
    try:
        # Convert input data to pandas Series
        dates = pd.to_datetime(request.data.dates)
        values = request.data.values
        data = pd.Series(values, index=dates)
        
        # Initialize SARIMA model with provided parameters
        model = SARIMAModel(
            order=request.order,
            seasonal_order=request.seasonal_order
        )
        
        # Train model
        model.train(data)
        
        # Make predictions
        predictions = model.predict(stock_data=data, n_steps=request.n_steps, start_idx=len(data))
        
        # Generate plot with both data and predictions
        plot_base64 = model.generate_plot(stock_data=data, predictions=predictions)
        
        # Format response
        forecast_dates = predictions.index.strftime('%Y-%m-%d').tolist()
        forecast_values = predictions.values.tolist()
        
        return {
            "forecast_dates": forecast_dates,
            "forecast_values": forecast_values,
            "plot_base64": plot_base64
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 