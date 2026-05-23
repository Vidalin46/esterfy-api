FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiarrequirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la app
COPY app/ ./app/
COPY .env .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
