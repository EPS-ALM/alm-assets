from fastapi import FastAPI
from assets.views.markowitz import markowitz
from assets.views.forecast_var_view import forecast_var
from assets.views.forecast_lstm_view import forecast_lstm
from assets.views.forecast_lstm_view import forecast_lstm

app = FastAPI()

app.include(forecast_lstm)
app.include_router(markowitz)
app.include_router(forecast_var)

@app.get("/")
def read_root():
    return {"message": "API de Gestão de Ativos"}
