from fastapi import FastAPI
from database import Base, engine
from views.item_view import router as item_router
from views.markowitz import markowitz
from views.forecast_var_view import forecast_var

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(item_router)
app.include_router(markowitz)
app.include_router(forecast_var)

@app.get("/")
def read_root():
    return {"message": "API de Gestão de Ativos"}
