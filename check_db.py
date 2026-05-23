from sqlalchemy import create_engine, inspect
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)

print("=== TABLA: receta ===")
for col in inspector.get_columns("receta"):
    print(f"{col['name']}: {col['type']}")

print("\n=== TABLA: cotizacion ===")
for col in inspector.get_columns("cotizacion"):
    print(f"{col['name']}: {col['type']}")

print("\n=== TABLA: pedido ===")
for col in inspector.get_columns("pedido"):
    print(f"{col['name']}: {col['type']}")
