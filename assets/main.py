from assets.views.markowitz import markowitz
from assets.views.forecast_var_view import forecast_var
from assets.views.hedge_view import hedge
from assets.views.forecast_sarima_view import forecast_sarima

from fastapi import FastAPI

app = FastAPI(
    title="Asset Management API",
    description="API for asset management and forecasting",
    version="1.0.0"
)

app.include_router(markowitz)
app.include_router(forecast_var)
app.include_router(hedge)
app.include_router(forecast_sarima)

@app.get("/")
def read_root():
    return {"message": "API de Gestão de Ativos"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 