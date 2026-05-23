from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# INVENTARIO
class Inventario(Base):
    __tablename__ = "inventario"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    cantidad = Column(Float)
    unidad_medida = Column(String(20))
    costo_producto = Column(Float)
    costo_unitario = Column(Float)
    fecha_registro = Column(DateTime)

# RECETA - matches exact database schema
class Receta(Base):
    __tablename__ = "receta"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    cantidad_usada = Column(Integer)
    costo_produccion = Column(Float)
    precio_venta = Column(Float)
    porcentaje_ganancia = Column(Float)
    ingredientes = Column(Text)  # JSON string para guardar ingredientes

# COTIZACION
class Cotizacion(Base):
    __tablename__ = "cotizacion"
    
    id = Column(Integer, primary_key=True)
    nombre_cliente = Column(String(150))
    telefono = Column(String(20))
    cantidad = Column(Integer)
    total = Column(Numeric(10, 2))
    id_receta = Column(Integer)
    fecha_cotizacion = Column(Date)

# PEDIDO - matches exact database schema
class Pedido(Base):
    __tablename__ = "pedido"
    
    id = Column(Integer, primary_key=True)
    id_cotizacion = Column(Integer, ForeignKey("cotizacion.id"))
    cliente = Column(String(255))
    producto = Column(String(255))
    cantidad = Column(Integer)
    total = Column(Float)
    estado = Column(String(50))
    fecha_pedido = Column(DateTime)
