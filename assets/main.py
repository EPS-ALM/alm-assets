from fastapi import FastAPI
from assets.views.markowitz import markowitz
from assets.views.forecast_var_view import forecast_var

app = FastAPI()

app.include_router(markowitz)
app.include_router(forecast_var)

@app.get("/")
def read_root():
    return {"message": "API de Gestão de Ativos"}
