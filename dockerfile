# Usa una imagen de Python como base
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación y los requisitos al contenedor
COPY ./app/requirements.txt ./app/requirements.txt

COPY ./app/__init__.py /app/
# Instala las dependencias de Python
RUN pip install -r ./app/requirements.txt

EXPOSE 93
# Expone el puerto 5000 para que Flask pueda recibir solicitudes
CMD ["python", "__init__.py"]