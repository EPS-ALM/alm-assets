from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.item_controller import create_item, get_items, get_item_by_id

router = APIRouter()

## Exemplo
@router.post("/items/")
def create_item_route(name: str, price: float, db: Session = Depends(get_db)):
    return create_item(db, name, price)

## Exemplo
@router.get("/items/")
def get_items_route(db: Session = Depends(get_db)):
    return get_items(db)

## Exemplo
@router.get("/items/{item_id}")
def get_item_route(item_id: int, db: Session = Depends(get_db)):
    item = get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
