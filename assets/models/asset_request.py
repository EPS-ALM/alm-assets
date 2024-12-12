from pydantic import BaseModel
from typing import List

class AssetRequest(BaseModel):
    tickers: List[str]  # Lista de símbolos dos ativos para análise