from fastapi import APIRouter

markowitz  = APIRouter()

@markowitz.get("/markowitz/")
def markowitz_root():
    return {"message": "markowitz"}