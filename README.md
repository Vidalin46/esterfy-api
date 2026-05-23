# API de Repostería

API REST para gestionar una repostería con FastAPI y PostgreSQL.

## Estructura

```
API/
├── app/
│   ├── __init__.py
│   ├── config.py      # Configuración
│   ├── database.py  # Conexión a DB
│   ├── models.py   # Modelos SQLAlchemy
│   └── main.py     # Endpoints API
├── .env            # Variables de entorno
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Endpoints

- **GET /** - Health check
- **GET /health** - Estado de la API

### Cotizaciones
- `GET /cotizaciones` - Listar todas
- `POST /cotizaciones` - Crear
- `GET /cotizaciones/{id}` - Obtener una
- `PUT /cotizaciones/{id}` - Actualizar
- `DELETE /cotizaciones/{id}` - Eliminar

### Inventario
- `GET /inventario`
- `POST /inventario`
- `GET /inventario/{id}`
- `PUT /inventario/{id}`
- `DELETE /inventario/{id}`

### Pedidos
- `GET /pedidos`
- `POST /pedidos`
- `GET /pedidos/{id}`
- `PUT /pedidos/{id}`
- `DELETE /pedidos/{id}`

### Recetas
- `GET /recetas`
- `POST /recetas`
- `GET /recetas/{id}`
- `PUT /recetas/{id}`
- `DELETE /recetas/{id}`

##Ejecutar con Docker

```bash
# Construir imagen
docker build -t api-reposteria .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env api-reposteria
```

O con docker-compose:

```bash
docker-compose up --build
```

##Ejecutar localmente (sin Docker)

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000

Documentación automática en: http://localhost:8000/docs
