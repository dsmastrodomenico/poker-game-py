# Usa una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del directorio actual al directorio /app en el contenedor
COPY . /app

# Comando para ejecutar el script Python cuando el contenedor se inicie
CMD ["python", "main.py"]