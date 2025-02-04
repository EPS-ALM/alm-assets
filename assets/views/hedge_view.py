from fastapi import APIRouter
from assets.controllers.hedge_controller import select_hedge_asset
from assets.models.asset_request import AssetRequest


hedge = APIRouter()

@hedge.post("/hedge/select")
def get_hedge_suggestion(asset_request: AssetRequest):
    """
    Endpoint para selecionar um ativo de hedge a partir de uma lista de ativos.
    Exemplo: /hedge/select?tickers=AAPL,MSFT,GOOGL
    """

    return select_hedge_asset(asset_request.tickers)