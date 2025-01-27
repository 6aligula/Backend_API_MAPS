# Aplicación para Gestión del Agua de los Agricultores de Málaga

## Descripción
Este repositorio alberga el código fuente de un Trabajo de Fin de Grado (TFG) que consiste en un backend desarrollado con Django y PostGIS como base de datos. La aplicación expone una API mediante contenedores Docker y Docker Compose, facilitando su portabilidad. Está destinada a la gestión eficiente del agua para las juntas de regantes.

## Resumen del Proyecto

### Objetivo del Proyecto
El objetivo es proporcionar una aplicación moderna, escalable y adaptable a nuevas tecnologías, incluyendo Inteligencia Artificial (IA), para las juntas de regantes de la provincia de Málaga y otras organizaciones con necesidades similares.

### Contexto y Justificación
Este proyecto surge de la necesidad de actualizar un sistema obsoleto actualmente en uso, reemplazándolo por una solución multiplataforma, escalable y moderna. La gestión rigurosa del agua es crucial dado el creciente desafío que representa su escasez. Este software es esencial, permitiendo la integración de información de dispositivos IoT para optimizar la agricultura mediante tecnologías avanzadas como Machine Learning, Deep Learning y IA especializada, proporcionando recomendaciones basadas en datos reales.

### Contribuciones
Agradecemos a la junta de regantes por su valioso feedback e información sobre sus necesidades, permitiendo adaptar la aplicación a sus requerimientos.

## Uso

### Requisitos Previos
- **Linux:** Docker y Docker Compose.
- **Mac:** Docker Desktop.
- **Windows:** Docker Desktop y Subsistema Windows para Linux (WSL).

Para entornos de producción, se recomienda el uso de un servidor Linux debido a su costo y compatibilidad nativa con Docker.

### Instrucciones
1. **Instalar Docker y Docker Compose.**
2. **Construir la Aplicación:**
   ```bash
   docker-compose up --build
   ```
3. **Acceder a la Consola de Administración de Django:**
   - URL: `http://localhost:8000/admin`
4. **Configurar Variables de Entorno:**
   - Modificar solo las variables necesarias para el envío de correos a través de Gmail.

### Ejemplo de Archivo .env
A continuación se muestra un ejemplo de configuración del archivo `.env`:

```env
SECRET_KEY=r6Rw6kEq12aAoWoACa52SOgZ096YnCV9X9YavUlhiYLsjGY8U93AtCd2KyFtYXX+bog=
ALLOWED_HOSTS=backstore.online,192.168.1.166,0.0.0.0,192.168.1.8,192.168.200.165,localhost
DEBUG=True
DB_ENGINE=django.contrib.gis.db.backends.postgis
DB_NAME=rastrea
DB_USER=cal
DB_PASSWORD=12345
DB_HOST=db
DB_PORT=5432
# Configuración del servidor de correo electrónico
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=admin@hola.com
EMAIL_HOST_PASSWORD=lapassword
```

## Tecnologías

### Lenguaje y Framework
- **Python** con **Django** utilizando su ORM.

### Base de Datos
- **PostGIS:** Extensión de PostgreSQL para datos geoespaciales.

### Contenerización
- **Docker:** Virtualización de aplicaciones.

### Asistencia de Código
- **ChatGPT 4-o Advance Voice:** Disponible solo en Mac ARM.

### Plataformas de Desarrollo
- Computadoras Linux y Mac.

### Documentación de Endpoints
- **Swagger**

### Bibliotecas Utilizadas
- **django.contrib.admin**
- **django.contrib.auth**
- **django.contrib.contenttypes**
- **django.contrib.sessions**
- **django.contrib.messages**
- **django.contrib.staticfiles**
- **django.contrib.gis**
- **drf_yasg**
- **leaflet**
- **rest_framework**
- **rest_framework_gis**
- **corsheaders**
- **django_extensions**
- **rest_framework_simplejwt**

## Autores
- **El Diablo GPT**

## Licencia

Este proyecto está licenciado bajo la Licencia Pública General de Affero de GNU con cláusulas adicionales. Para cualquier uso comercial, es necesario obtener una licencia comercial del autor. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

# Esquema de base de datos
```
+-----------------------+       +------------------------+       +-----------------------------+
|        User           |       |         Plot           |       |    CaracteristicasParcela   |
|-----------------------|       |------------------------|       |-----------------------------|
| - id (Primary Key)    |<-M2M->| - id (Primary Key)     |<-1to1-| - id (Primary Key)          |
| - username            |       | - name                 |       | - plot (OneToOne with Plot) |
| - email               |       | - bounds (PolygonField)|       | - identificacion            |
| ...                   |       |                        |       | - parcela_catastral         |
+-----------------------+       |                        |       | - sup_total                 |
                                 |                        |       | - sup_regable               |
                                 |                        |       | - num_olivos                |
                                 +------------------------+       | - concesion                |
                                                                  | - toma_agua                |
                                                                  | - suelo                    |
                                                                  | - paraje                   |
                                                                  | - fecha_alta               |
                                                                  +-----------------------------+
                                                                            |
                                                                            |
                           +------------------------+                       |
                           |       UsoParcela       |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - cultivo (ForeignKey) |
                           | - superficie           |
                           | - sistema_riego        |
                           | - estado               |
                           | - fecha_alta           |
                           | - fecha_baja           |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |  ContadoresMedidas     |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - contador             |
                           | - fecha_alta           |
                           | - fecha_baja           |
                           | - lectura_max          |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |       Consumos         |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - numero_factura       |
                           | - periodo_facturacion  |
                           | - volumen_medido       |
                           | - comentario           |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |   DatosAdicionales     |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - tipo_dato            |
                           | - valor                |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |     ControlPagos       |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - factura              |
                           | - numero_factura       |
                           | - pagador              |
                           | - vencimiento          |
                           | - total                |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |       Factura          |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - numero_factura       |
                           | - fecha_emision        |
                           | - fecha_vencimiento    |
                           | - subtotal             |
                           | - recargo              |
                           | - total_facturado      |
                           | - estado               |
                           | - fecha_pago           |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |     LineaFactura       |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - factura (ForeignKey) |-----------------------+
                           | - concepto             |
                           | - unidades             |
                           | - precio_unitario      |
                           | - iva                  |
                           | - total                |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |       Cultivo          |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - nombre               |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |     FaseCultivo        |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - cultivo (ForeignKey) |-----------------------+
                           | - fase                 |
                           | - kc                   |
                           | - nap                  |
                           | - prof_rad             |
                           | - das_inicio           |
                           | - porcentaje_almacen   |
                           +------------------------+
```

### Explicación de las Relaciones

1. **User**
   - Relación **Muchos a Muchos** con **Plot**.
   - Relación **Uno a Muchos** con **Incidencia**, **Peticion**, **RegistroDocumento**, y **Perfil**.

2. **Plot**
   - Relación **Muchos a Muchos** con **User**.
   - Relación **Uno a Uno** con **CaracteristicasParcela**.

3. **CaracteristicasParcela**
   - Relación **Uno a Uno** con **Plot**.
   - Relación **Uno a Muchos** con **UsoParcela**, **ContadoresMedidas**, **Consumos**, **DatosAdicionales**, **ControlPagos**, y **Factura**.

4. **UsoParcela**
   - Relación **Muchos a Uno** con **CaracteristicasParcela**.
   - Relación **Muchos a Uno** con **Cultivo**.

5. **ContadoresMedidas**
   - Relación **Muchos a Uno** con **CaracteristicasParcela**.

6. **Consumos**
   - Relación **Muchos a Uno** con **CaracteristicasParcela**.

7. **DatosAdicionales**
   - Relación **Muchos a Uno** con **CaracteristicasParcela**.

8. **ControlPagos**
   - Relación **Muchos a Uno** con **CaracteristicasParcela**.

9. **Cultivo**
   - Relación **Uno a Muchos** con **FaseCultivo**.
   - Relación **Uno a Muchos** con **UsoParcela**.

10. **FaseCultivo**
    - Relación **Muchos a Uno** con **Cultivo**.

11. **Factura**
    - Relación **Muchos a Uno** con **CaracteristicasParcela**.
    - Relación **Uno a Muchos** con **LineaFactura**.

12. **LineaFactura**
    - Relación **Muchos a Uno** con **Factura**.

13. **Perfil**
    - Relación **Uno a Uno** con **User**.
    - Relación **Muchos a Muchos** con **ComunidadRegantes**.
