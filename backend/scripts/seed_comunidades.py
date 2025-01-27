# seed_comunidades.py

import os
from backend.models import ComunidadRegantes

def create_comunidades():
    comunidades_data = [
        {
            "nombre": "Comunidad de Regantes del Guadalquivir",
            "cif": "G12345678",
            "direccion": "avenida del río 1",
            "localidad": "sevilla",
            "codigo_postal": "41001",
            "telefono_fijo": "954123456",
            "telefono_movil": "600123456",
            "email_alternativo": "contacto@guadalquivir.com",
            "nombre_entidad": "Santander",
            "numero_banco": "0049",
            "numero_sucursal": "210",
            "digito_control": "5",
            "numero_cuenta": "0009876543",
            "cargo": "Gestión de Aguas",
            "telefono_contacto": "600123456",
            "email_contacto": "contacto@guadalquivir.com",
            "telefono_movil_contacto": "600123456"
        },
        {
            "nombre": "Comunidad de Regantes del Segura",
            "cif": "G87654321",
            "direccion": "plaza del agua 3",
            "localidad": "murcia",
            "codigo_postal": "30004",
            "telefono_fijo": "968123456",
            "telefono_movil": "600654321",
            "email_alternativo": "info@segura.com",
            "nombre_entidad": "BBVA",
            "numero_banco": "0182",
            "numero_sucursal": "350",
            "digito_control": "7",
            "numero_cuenta": "0006543212",
            "cargo": "Administración",
            "telefono_contacto": "600654321",
            "email_contacto": "info@segura.com",
            "telefono_movil_contacto": "600654321"
        },
        {
            "nombre": "Comunidad de Regantes del Tajo",
            "cif": "G23456789",
            "direccion": "calle del río 5",
            "localidad": "toledo",
            "codigo_postal": "45002",
            "telefono_fijo": "925123456",
            "telefono_movil": "600987654",
            "email_alternativo": "admin@tajo.com",
            "nombre_entidad": "La Caixa",
            "numero_banco": "2034",
            "numero_sucursal": "300",
            "digito_control": "6",
            "numero_cuenta": "0001237654",
            "cargo": "Gestión de Recursos",
            "telefono_contacto": "600987654",
            "email_contacto": "admin@tajo.com",
            "telefono_movil_contacto": "600987654"
        }
    ]

    for comunidad_data in comunidades_data:
        try:
            comunidad, created = ComunidadRegantes.objects.get_or_create(**comunidad_data)
            if created:
                print(f'Comunidad creada: {comunidad.nombre}')
            else:
                print(f'Comunidad ya existente: {comunidad.nombre} - No se creó de nuevo')
        except Exception as e:
            print(f'Error al procesar la comunidad {comunidad_data["nombre"]}: {e}')

def run():
    create_comunidades()

