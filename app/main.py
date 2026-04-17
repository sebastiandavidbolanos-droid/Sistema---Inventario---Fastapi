from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, database

# 1. Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

# 2. Definir la instancia de FastAPI (ESTA ES LA LÍNEA QUE BUSCA UVICORN)
app = FastAPI(title="Sistema de Inventario")

@app.get("/")
def home():
    return {"status": "Sistema Online", "message": "Bienvenido a la API de Inventario"}

@app.get("/products/", response_model=List[schemas.Product])
def list_products(db: Session = Depends(database.get_db)):
    return crud.get_products(db)

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product