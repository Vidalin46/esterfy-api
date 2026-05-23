import logging
import json
from datetime import date
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict

class InventarioSchema(BaseModel):
    nombre: str | None = None
    cantidad: float | None = None
    unidad_medida: str | None = None
    costo_producto: float | None = None
    costo_unitario: float | None = None
    model_config = ConfigDict(from_attributes=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.database import get_db
from app.models import Inventario, Receta, Cotizacion, Pedido

app = FastAPI(
    title="API Esterfy Bakery",
    description="API para gestionar inventario, recetas, cotizaciones y pedidos de Esterfy Bakery",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ESQUEMAS PYDANTIC ---

class RecetaSchema(BaseModel):
    nombre: str | None = None
    cantidad_usada: int | None = None
    costo_produccion: float | None = None
    precio_venta: float | None = None
    porcentaje_ganancia: float | None = None
    ingredientes: list | None = None  # JSON array for ingredients
    model_config = ConfigDict(from_attributes=True)

class CotizacionSchema(BaseModel):
    nombre_cliente: str | None = None
    telefono: str | None = None
    cantidad: int | None = None
    total: float | None = None
    id_receta: int | None = None
    # fecha_cotizacion se genera automáticamente, no se acepta en POST
    model_config = ConfigDict(from_attributes=True)

class PedidoSchema(BaseModel):
    id_cotizacion: int | None = None
    cliente: str | None = None
    producto: str | None = None
    cantidad: int | None = None
    total: float | None = None
    estado: str | None = "pendiente"
    fecha_pedido: str | None = None
    model_config = ConfigDict(from_attributes=True)

# --- RUTAS INVENTARIO ---

@app.get("/inventario")
def get_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@app.post("/inventario")
def create_inventario(inventario: InventarioSchema, db: Session = Depends(get_db)):
    data = inventario.model_dump()
    
    # Calcular costo_unitario automáticamente
    if data.get('costo_producto') and data.get('cantidad') and data.get('cantidad') > 0:
        data['costo_unitario'] = data['costo_producto'] / data['cantidad']
    
    db_inventario = Inventario(**data)
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

@app.delete("/inventario/{inventario_id}")
def delete_inventario(inventario_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    db.delete(inventario)
    db.commit()
    return {"message": "Inventario eliminado"}

# --- RUTAS RECETAS ---

@app.get("/recetas")
def get_recetas(db: Session = Depends(get_db)):
    recetas = db.query(Receta).all()
    # Convertir ingredientes JSON a lista para cada receta
    results = []
    for r in recetas:
        rec_dic = {
            "id": r.id,
            "nombre": r.nombre,
            "cantidad_usada": r.cantidad_usada,
            "costo_produccion": r.costo_produccion,
            "precio_venta": r.precio_venta,
            "porcentaje_ganancia": r.porcentaje_ganancia,
            "ingredientes": json.loads(r.ingredientes) if r.ingredientes else []
        }
        results.append(rec_dic)
    return results

@app.post("/recetas")
def create_receta(receta: RecetaSchema, db: Session = Depends(get_db)):
    data = receta.model_dump()
    # Convertir ingredientes a JSON string
    if data.get('ingredientes'):
        data['ingredientes'] = json.dumps(data['ingredientes'])
    db_receta = Receta(**data)
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta

@app.get("/recetas/{receta_id}")
def get_receta(receta_id: int, db: Session = Depends(get_db)):
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    # Convertir ingredientes JSON a lista
    return {
        "id": receta.id,
        "nombre": receta.nombre,
        "cantidad_usada": receta.cantidad_usada,
        "costo_produccion": receta.costo_produccion,
        "precio_venta": receta.precio_venta,
        "porcentaje_ganancia": receta.porcentaje_ganancia,
        "ingredientes": json.loads(receta.ingredientes) if receta.ingredientes else []
    }

@app.put("/recetas/{receta_id}")
def update_receta(receta_id: int, receta: RecetaSchema, db: Session = Depends(get_db)):
    db_receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not db_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    data = receta.model_dump()
    # Convertir ingredientes a JSON string
    if data.get('ingredientes'):
        data['ingredientes'] = json.dumps(data['ingredientes'])
    for key, value in data.items():
        setattr(db_receta, key, value)
    db.commit()
    db.refresh(db_receta)
    # Return in same format as get_recetas
    return {
        "id": db_receta.id,
        "nombre": db_receta.nombre,
        "cantidad_usada": db_receta.cantidad_usada,
        "costo_produccion": db_receta.costo_produccion,
        "precio_venta": db_receta.precio_venta,
        "porcentaje_ganancia": db_receta.porcentaje_ganancia,
        "ingredientes": json.loads(db_receta.ingredientes) if db_receta.ingredientes else []
    }

@app.delete("/recetas/{receta_id}")
def delete_receta(receta_id: int, db: Session = Depends(get_db)):
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    db.delete(receta)
    db.commit()
    return {"message": "Receta eliminada"}

# --- RUTAS COTIZACIONES ---

@app.get("/cotizaciones")
def get_cotizaciones(db: Session = Depends(get_db)):
    cotizaciones = db.query(Cotizacion).all()
    results = []
    for c in cotizaciones:
        # Buscar los datos de la receta asociada
        receta = db.query(Receta).filter(Receta.id == c.id_receta).first() if c.id_receta else None
        cotizacion_data = {
            "id": c.id,
            "nombre_cliente": c.nombre_cliente,
            "telefono": c.telefono,
            "cantidad": c.cantidad,
            "total": float(c.total) if c.total else 0,
            "id_receta": c.id_receta,
            "fecha_cotizacion": c.fecha_cotizacion.isoformat() if c.fecha_cotizacion else None
        }
        # Agregar datos de la receta si existe
        if receta:
            cotizacion_data["receta"] = {
                "id": receta.id,
                "nombre": receta.nombre,
                "cantidad_usada": receta.cantidad_usada,
                "costo_produccion": float(receta.costo_produccion) if receta.costo_produccion else 0,
                "precio_venta": float(receta.precio_venta) if receta.precio_venta else 0,
                "porcentaje_ganancia": float(receta.porcentaje_ganancia) if receta.porcentaje_ganancia else 0,
                "ingredientes": json.loads(receta.ingredientes) if receta.ingredientes else []
            }
        else:
            cotizacion_data["receta"] = None
        results.append(cotizacion_data)
    return results

@app.post("/cotizaciones")
def create_cotizacion(cotizacion: CotizacionSchema, db: Session = Depends(get_db)):
    data = cotizacion.model_dump()
    # Agregar fecha automáticamente
    data['fecha_cotizacion'] = date.today()
    db_cotizacion = Cotizacion(**data)
    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)
    return db_cotizacion

@app.get("/cotizaciones/{cotizacion_id}")
def get_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return cotizacion

@app.put("/cotizaciones/{cotizacion_id}")
def update_cotizacion(cotizacion_id: int, cotizacion: CotizacionSchema, db: Session = Depends(get_db)):
    db_cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not db_cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    for key, value in cotizacion.model_dump().items():
        setattr(db_cotizacion, key, value)
    db.commit()
    db.refresh(db_cotizacion)
    return db_cotizacion

@app.delete("/cotizaciones/{cotizacion_id}")
def delete_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    db.delete(cotizacion)
    db.commit()
    return {"message": "Cotización eliminada"}

# --- RUTAS PEDIDOS ---

@app.get("/pedidos")
def get_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

@app.post("/pedidos")
def create_pedido(pedido: PedidoSchema, db: Session = Depends(get_db)):
    db_pedido = Pedido(**pedido.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.get("/pedidos/{pedido_id}")
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@app.put("/pedidos/{pedido_id}")
def update_pedido(pedido_id: int, pedido: PedidoSchema, db: Session = Depends(get_db)):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in pedido.model_dump().items():
        setattr(db_pedido, key, value)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.delete("/pedidos/{pedido_id}")
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido)
    db.commit()
    return {"message": "Pedido eliminado"}

# --- HEALTH CHECK ---
@app.get("/")
def root():
    return {"message": "API de Esterfy Bakery funcionando", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
