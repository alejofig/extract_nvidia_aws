FROM nvidia/cuda:11.8-base

# Instalar dependencias
RUN apt-get update && apt-get install -y python3 python3-pip nv-ingest

# Copiar el código
COPY . /app
WORKDIR /app

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Exponer el puerto para FastAPI
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
