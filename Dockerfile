# Utiliza una imagen oficial de Python como padre
FROM python:3.8

# Instala las dependencias necesarias para GeoDjango: GDAL, GEOS, PROJ
RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin libgdal-dev && \
    apt-get install -y netcat-openbsd  # netcat ya estaba siendo instalado
    
# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido del directorio actual en el contenedor en /app
ADD . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Establecer la variable de entorno para desactivar el buffering de Python
# dejar ENV PYTHONUNBUFFERED 1 en producción no es inherentemente malo y puede ser beneficioso para ciertos tipos de aplicaciones, 
# especialmente aquellas donde la inmediatez de la salida de logs es importante. 
ENV PYTHONUNBUFFERED 1

# Abre el puerto 8000 para que el contenedor sea accesible desde afuera
EXPOSE 8000

# Instala netcat-openbsd para que funcione el script de wait-for.sh
RUN apt-get update && apt-get install -y netcat-openbsd

# Da permisos de ejecución a los scripts
RUN chmod +x /app/start.sh
RUN chmod +x /app/wait-for.sh

# Define el comando que se ejecutará al iniciar el contenedor
CMD ["/app/start.sh"]

