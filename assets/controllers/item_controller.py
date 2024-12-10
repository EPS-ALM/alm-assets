from sqlalchemy.orm import Session
from models.item import Item


## Exemplo
def create_item(db: Session, name: str, price: float) -> Item:
    item = Item(name=name, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


## Exemplo
def get_items(db: Session):
    return db.query(Item).all()


## Exemplo
def get_item_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()
