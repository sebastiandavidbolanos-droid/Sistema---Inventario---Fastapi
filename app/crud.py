from sqlalchemy.orm import Session
from . import models, schemas

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    # Usamos model_dump() para Pydantic v2
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product