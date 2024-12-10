from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem vindo a API de Gestão de ativos"}
