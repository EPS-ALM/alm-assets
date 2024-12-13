from fastapi import APIRouter, HTTPException
from assets.controllers.markowitz_controller import get_optimal_allocations
from assets.models.asset_request import AssetRequest
markowitz  = APIRouter()

@markowitz.post("/markowitz/")
def markowitz_root(asset_request: AssetRequest):
    try:
        portfolio, plt_base64 = get_optimal_allocations(asset_request.tickers)

        portfolio_array = [{"ticker": ticker, "allocation": allocation} for ticker, allocation in portfolio.items()]

        return {
            "portfolio": portfolio_array,
            "plot_base64": plt_base64
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # Exibe o rastreamento completo no log do console
        raise HTTPException(status_code=400, detail=str(e))