import os
from django.contrib.auth.models import User
from backend.models import Perfil, ComunidadRegantes

def create_users():

    # Asegúrate de que las comunidades ya estén creadas antes de ejecutar esta función
    comunidad1 = ComunidadRegantes.objects.get(nombre="Comunidad de Regantes del Guadalquivir")
    comunidad2 = ComunidadRegantes.objects.get(nombre="Comunidad de Regantes del Segura")
    comunidad3 = ComunidadRegantes.objects.get(nombre="Comunidad de Regantes del Tajo")

    users_data = [
        {
            "username": "12345678k",
            "password": "1234Abcd!",
            "email": "juan@gmail.com",
            "first_name": "Juan",
            "is_staff": "False",
            "comunidades": [comunidad1, comunidad2],
            "perfil": {
                "cif": "87654321l",
                "direccion": "calle manzanares 12",
                "localidad": "malaga",
                "codigo_postal": "05412",
                "telefono_fijo": "987564324",
                "telefono_movil": "654987234",
                "email_alternativo": "alter@gmail.com",
                "nombre_entidad": "La caixa",
                "numero_banco": "2034",
                "numero_sucursal": "300",
                "digito_control": "6",
                "numero_cuenta": "0001237654",
                "cargo": "Analista de Olivos",
                "telefono_contacto": "675435634",
                "email_contacto": "juan.perez@ejemplo.com",
                "telefono_movil_contacto": "654345232"
            }
        },
        {
            "username": "87654321j",
            "password": "1234Abcd!",
            "email": "maria@gmail.com",
            "first_name": "Maria",
            "is_staff": "False",
            "comunidades": [comunidad2],
            "perfil": {
                "cif": "12345678m",
                "direccion": "avenida granada 15",
                "localidad": "sevilla",
                "codigo_postal": "01005",
                "telefono_fijo": "965847123",
                "telefono_movil": "612345678",
                "email_alternativo": "m.altern@gmail.com",
                "nombre_entidad": "Santander",
                "numero_banco": "0049",
                "numero_sucursal": "210",
                "digito_control": "5",
                "numero_cuenta": "0009876543",
                "cargo": "Directora de Proyectos",
                "telefono_contacto": "689123456",
                "email_contacto": "maria.garcia@ejemplo.com",
                "telefono_movil_contacto": "699876543"
            }
        },
        {
            "username": "23456789h",
            "password": "1234Abcd!",
            "email": "luis@gmail.com",
            "first_name": "Luis",
            "is_staff": "True",
            "comunidades": [comunidad3],
            "perfil": {
                "cif": "87654321n",
                "direccion": "calle naranjo 20",
                "localidad": "cordoba",
                "codigo_postal": "14005",
                "telefono_fijo": "957123456",
                "telefono_movil": "600123456",
                "email_alternativo": "l.altern@gmail.com",
                "nombre_entidad": "BBVA",
                "numero_banco": "0182",
                "numero_sucursal": "350",
                "digito_control": "7",
                "numero_cuenta": "0006543212",
                "cargo": "Ingeniero de Sistemas",
                "telefono_contacto": "665432189",
                "email_contacto": "luis.fernandez@ejemplo.com",
                "telefono_movil_contacto": "610987654"
            }
        }
    ]

    for user_data in users_data:
        try:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                is_staff=user_data["is_staff"]
            )
            if created:
                print(f'Usuario creado: {user.username}')
                user.set_password(user_data["password"])
                user.save()
                print(f'Usuario {user.username} guardado con éxito.')
                perfil_data = user_data["perfil"]
                perfil, perfil_created = Perfil.objects.get_or_create(usuario=user, **perfil_data)
                if perfil_created:
                    print(f'Perfil creado para: {user.username}')
                    # Asignar comunidades al perfil
                    perfil.comunidades_regantes.set(user_data["comunidades"])
                    perfil.save()
                    print(f'Comunidades asignadas al perfil de {user.username}')
                else:
                    print(f'Error al crear el perfil para: {user.username}')
            else:
                print(f'Usuario ya existente: {user.username} - No se creó de nuevo')
        except Exception as e:
            print(f'Error al procesar el usuario {user_data["username"]}: {e}')

def run():
    create_users()