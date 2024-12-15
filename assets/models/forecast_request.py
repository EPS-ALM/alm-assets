from pydantic import BaseModel

class ForecastRequest(BaseModel):
    ticker: str  # Símbolo do ativo para previsão