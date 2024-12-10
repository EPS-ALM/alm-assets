from fastapi import FastAPI
from database import Base, engine
from views.item_view import router as item_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(item_router)

@app.get("/")
def read_root():
    return {"message": "API de Gestão de Ativos"}
