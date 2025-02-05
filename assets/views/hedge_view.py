from fastapi import APIRouter
from assets.controllers.hedge_controller import get_hedges
from assets.models.asset_request import AssetRequest


hedge = APIRouter()

@hedge.post("/hedge/select")
def get_hedge_suggestion(asset_request: AssetRequest):
    """
    Endpoint para selecionar um ativo de hedge a partir de uma lista de ativos.
    Exemplo: /hedge/select?tickers=AAPL,MSFT,GOOGL
    """

    return get_hedges(asset_request.tickers)