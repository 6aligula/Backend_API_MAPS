#!/bin/bash
# start.sh

# Solo calcula HOST_IP si DJANGO_ALLOWED_HOSTS no está ya definido
if [ -z "$DJANGO_ALLOWED_HOSTS" ]; then
  # Obtiene la dirección IP del host de alguna manera
  HOST_IP=$(hostname -I | awk '{print $1}')

  # Si no se pudo obtener la IP, usa 'localhost'
  if [ -z "$HOST_IP" ]; then
    HOST_IP="localhost"
  fi

  # Exporta la dirección IP a una variable de entorno para Django
  export DJANGO_ALLOWED_HOSTS=$HOST_IP,localhost
else
  # Utiliza DJANGO_ALLOWED_HOSTS como está, asumiendo que start_project.sh lo ha configurado
  export DJANGO_ALLOWED_HOSTS
fi

# Primero, utiliza wait-for.sh para esperar a que PostgreSQL esté listo
/app/wait-for.sh db:5432 -- echo "Database is up"

# Ejecuta las migraciones de Django
python manage.py makemigrations
python manage.py migrate --noinput

# Verifica que las migraciones se hayan aplicado correctamente
if [ $? -ne 0 ]; then
  echo "Error applying migrations"
  exit 1
fi

# Crea el superusuario de Django
python manage.py shell < create_superuser.py

# Verifica que el superusuario se haya creado correctamente
if [ $? -ne 0 ]; then
  echo "Error creating superuser"
  exit 1
fi

# Ejecuta el script de semilla de usuarios
python manage.py runscript seed_comunidades

# Verifica que el script de semilla de usuarios se haya ejecutado correctamente
if [ $? -ne 0 ]; then
  echo "Error running seed_comunidades script"
  exit 1
fi

# Ejecuta el script de semilla de usuarios
python manage.py runscript seed

# Verifica que el script de semilla de usuarios se haya ejecutado correctamente
if [ $? -ne 0 ]; then
  echo "Error running seed script"
  exit 1
fi

# Ejecuta el script de semilla de parcelas
python manage.py runscript seedCultivo

# Verifica que el script de semilla de parcelas se haya ejecutado correctamente
if [ $? -ne 0 ]; then
  echo "Error running seedCultivo script"
  exit 1
fi
# Ejecuta el script de semilla de parcelas
python manage.py runscript seedParcela

# Verifica que el script de semilla de parcelas se haya ejecutado correctamente
if [ $? -ne 0 ]; then
  echo "Error running seedParcela script"
  exit 1
fi

# Inicia el servidor de desarrollo de Django
python manage.py runserver 0.0.0.0:8000
