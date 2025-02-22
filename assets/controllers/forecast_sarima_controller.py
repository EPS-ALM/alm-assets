import pandas as pd
import numpy as np
from fastapi import HTTPException
from modelos.SARIMA import SARIMAModel
from assets.models.forecast_sarima_model import ForecastRequest
import yfinance as yf
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def get_historical_data(ticker: str, days: int) -> pd.Series:
    """Fetch historical data for the given ticker"""
    try:
        # Calculate start date
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        logger.debug(f"Fetching data for {ticker} from {start_date} to {end_date}")
        
        # Fetch data from Yahoo Finance
        ticker_data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )
        
        if ticker_data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
            
        # Get the Close price series and set its name
        close_prices = ticker_data['Close']
        close_prices.name = ticker  # Set the name attribute instead of returning it separately
        
        # Ensure we have a 1D Series
        if isinstance(close_prices, pd.DataFrame):
            close_prices = close_prices.squeeze()
        
        logger.debug(f"Data shape: {close_prices.shape}")
        logger.debug(f"Data type: {type(close_prices)}")
        logger.debug(f"Values type: {type(close_prices.values)}")
        logger.debug(f"Values shape: {close_prices.values.shape}")
        
        return close_prices
        
    except Exception as e:
        logger.error(f"Error in get_historical_data: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching data for {ticker}: {str(e)}"
        )

async def generate_forecast(request: ForecastRequest):
    """Generate forecast using SARIMA model"""
    try:
        # Fetch historical data
        data = await get_historical_data(request.ticker, request.days)
        
        logger.debug(f"Received data shape: {data.shape}")
        logger.debug(f"Received data type: {type(data)}")
        logger.debug(f"Received data index type: {type(data.index)}")
        
        # Initialize SARIMA model with provided parameters
        model = SARIMAModel(
            order=request.order,
            seasonal_order=request.seasonal_order
        )
        
        # Train model
        model.train(data)
        
        # Make predictions
        predictions = model.predict(
            stock_data=data,
            n_steps=request.n_steps,
            start_idx=len(data)
        )
        
        logger.debug(f"Predictions shape: {predictions.shape}")
        logger.debug(f"Predictions type: {type(predictions)}")
        logger.debug(f"Predictions index type: {type(predictions.index)}")
        
        # Generate plot with both data and predictions
        plot_base64 = model.generate_plot(
            stock_data=data, 
            predictions=predictions,
            name=data.name  # Use the name from the series
        )
        
        # Calculate metrics
        metrics = model.calculate_metrics(data)
        
        # Format response
        forecast_dates = [d.strftime('%Y-%m-%d') if hasattr(d, 'strftime') else str(d) 
                         for d in predictions.index]
        forecast_values = predictions.values.tolist()
        
        return {
            "forecast_dates": forecast_dates,
            "forecast_values": forecast_values,
            "plot_base64": plot_base64,
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Error in generate_forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 