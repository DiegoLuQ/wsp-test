# Usa una imagen de Python como base
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación y los requisitos al contenedor
COPY .main.py /app
COPY requirements.txt /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expone el puerto 5000 para que Flask pueda recibir solicitudes
# EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "main.py"]