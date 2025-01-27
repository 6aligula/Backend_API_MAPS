import os
from django.contrib.auth.models import User
from django.contrib.gis.geos import Polygon, LinearRing
from backend.models import CaracteristicasParcela, UsoParcela, ContadoresMedidas, Consumos, DatosAdicionales, ControlPagos, Plot, Cultivo

def create_plot(plot_data):
    try:
        coordinates = plot_data["coordinates"]
        print(f"Processing plot: {plot_data['name']}")
        print(f"Coordinates: {coordinates}")

        if not coordinates or not coordinates[0] or len(coordinates[0]) < 4:
            raise ValueError("LinearRing requires at least 4 points.")
        
        # Ensure the first and last point are the same to close the LinearRing
        if coordinates[0][0] != coordinates[0][-1]:
            coordinates[0].append(coordinates[0][0])
        
        # Convert coordinates to a LinearRing before creating the Polygon
        ring = LinearRing(coordinates[0])
        bounds = Polygon(ring)
        plot, created = Plot.objects.get_or_create(name=plot_data["name"], bounds=bounds)
        return plot, created
    except Exception as e:
        print(f"Error creating plot: {e}")
        return None, False


def create_related_models(caracteristicas, usos, contadores, consumos, datos, pagos):
    for uso in usos:
        cultivo = Cultivo.objects.get(nombre=uso.pop("cultivo"))
        UsoParcela.objects.get_or_create(parcela=caracteristicas, cultivo=cultivo, **uso)
    
    ContadoresMedidas.objects.bulk_create([ContadoresMedidas(parcela=caracteristicas, **contador) for contador in contadores], ignore_conflicts=True)
    Consumos.objects.bulk_create([Consumos(parcela=caracteristicas, **consumo) for consumo in consumos], ignore_conflicts=True)
    DatosAdicionales.objects.bulk_create([DatosAdicionales(parcela=caracteristicas, **dato) for dato in datos], ignore_conflicts=True)
    ControlPagos.objects.bulk_create([ControlPagos(parcela=caracteristicas, **pago) for pago in pagos], ignore_conflicts=True)

def create_parcelas():
    parcelas_data = [
        {
            "username": "12345678k",
            "plot": {
                "name": "Parcela Ejemplo 1",
                "coordinates": [[
                    [2.029752, 41.301370],
                    [2.032340, 41.302352],
                    [2.033241, 41.30118503],
                    [2.030672, 41.300052],
                    [2.029752, 41.301370]
                ]]
            },
            "caracteristicas": {
                "identificacion": "01-1",
                "parcela_catastral": "140707-001-003",
                "sup_total": 2.0000,
                "sup_regable": 1.7000,
                "num_olivos": 1200,
                "concesion": "Con concesión",
                "toma_agua": "Agr. 1",
                "suelo": "Suelo Franco",
                "paraje": "Valle Superior",
                "fecha_alta": "2001-10-18"
            },
            "usos_parcela": [
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Algodón",
                    "superficie": 1.0,
                    "sistema_riego": "Goteo",
                    "estado": "Activo",
                    "fecha_alta": "2001-10-18",
                    "fecha_baja": None
                },
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Maíz",
                    "superficie": 0.5,
                    "sistema_riego": "Goteo",
                    "estado": "Activo",
                    "fecha_alta": "2001-10-18",
                    "fecha_baja": None
                }
            ],
            "contadores_medidas": [
                {
                    "contador": "001003",
                    "fecha_alta": "2002-11-15",
                    "fecha_baja": None,
                    "lectura_max": 1000000
                }
            ],
            "consumos": [
                {
                    "numero_factura": "FAC001",
                    "periodo_facturacion": "2011-09",
                    "volumen_medido": 15000,
                    "comentario": "Consumo de riego"
                }
            ],
            "datos_adicionales": [
                {
                    "tipo_dato": "PH del suelo",
                    "valor": "7.0"
                }
            ],
            "control_pagos": [
                {
                    "factura": "FP001",
                    "numero_factura": "FAC001",
                    "pagador": "Juan Perez",
                    "vencimiento": "2011-09-30",
                    "total": 1000.00
                }
            ]
        },
        {
            "username": "12345678k",  # El mismo usuario para la segunda parcela
            "plot": {
                "name": "Parcela Ejemplo 4",
                "coordinates": [[
                    [2.059752, 41.331370],
                    [2.062340, 41.332352],
                    [2.063241, 41.33118503],
                    [2.060672, 41.330052],
                    [2.059752, 41.331370]
                ]]
            },
            "caracteristicas": {
                "identificacion": "04-1",
                "parcela_catastral": "170707-004-007",
                "sup_total": 3.0000,
                "sup_regable": 2.5000,
                "num_olivos": 900,
                "concesion": "Sin concesión",
                "toma_agua": "Agr. 4",
                "suelo": "Suelo Franco-Arenoso",
                "paraje": "Valle Oeste",
                "fecha_alta": "2007-12-22"
            },
            "usos_parcela": [
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Patata temprana",
                    "superficie": 1.5,
                    "sistema_riego": "Aspersión",
                    "estado": "Activo",
                    "fecha_alta": "2007-12-22",
                    "fecha_baja": None
                },
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Girasol",
                    "superficie": 1.0,
                    "sistema_riego": "Aspersión",
                    "estado": "Activo",
                    "fecha_alta": "2007-12-22",
                    "fecha_baja": None
                }
            ],
            "contadores_medidas": [
                {
                    "contador": "004007",
                    "fecha_alta": "2008-01-10",
                    "fecha_baja": None,
                    "lectura_max": 750000
                }
            ],
            "consumos": [
                {
                    "numero_factura": "FAC004",
                    "periodo_facturacion": "2014-10",
                    "volumen_medido": 20000,
                    "comentario": "Consumo de riego"
                }
            ],
            "datos_adicionales": [
                {
                    "tipo_dato": "PH del suelo",
                    "valor": "6.8"
                }
            ],
            "control_pagos": [
            {
                "factura": "FP004",
                "numero_factura": "FAC004",
                "pagador": "Carlos Lopez",
                "vencimiento": "2014-10-31",
                "total": 1500.00
            }
        ]
        },
        {
            "username": "87654321j",
            "plot": {
                "name": "Parcela Ejemplo 2",
                "coordinates": [[
                    [2.039752, 41.311370],
                    [2.042340, 41.312352],
                    [2.043241, 41.31118503],
                    [2.040672, 41.310052],
                    [2.039752, 41.311370]
                ]]
            },
            "caracteristicas": {
                "identificacion": "02-1",
                "parcela_catastral": "150808-002-004",
                "sup_total": 3.5000,
                "sup_regable": 3.0000,
                "num_olivos": 1500,
                "concesion": "Sin concesión",
                "toma_agua": "Agr. 2",
                "suelo": "Suelo Arenoso",
                "paraje": "Valle Inferior",
                "fecha_alta": "2005-05-15"
            },
            "usos_parcela": [
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Trigo",
                    "superficie": 2.0,
                    "sistema_riego": "Aspersión",
                    "estado": "Activo",
                    "fecha_alta": "2005-05-15",
                    "fecha_baja": None
                },
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Ajo",
                    "superficie": 1.0,
                    "sistema_riego": "Aspersión",
                    "estado": "Activo",
                    "fecha_alta": "2005-05-15",
                    "fecha_baja": None
                }
            ],
            "contadores_medidas": [
                {
                    "contador": "002004",
                    "fecha_alta": "2006-03-10",
                    "fecha_baja": None,
                    "lectura_max": 500000
                }
            ],
            "consumos": [
                {
                    "numero_factura": "FAC002",
                    "periodo_facturacion": "2012-10",
                    "volumen_medido": 25000,
                    "comentario": "Consumo de riego"
                }
            ],
            "datos_adicionales": [
                {
                    "tipo_dato": "Nivel de Nitrógeno",
                    "valor": "3.5"
                }
            ],
            "control_pagos": [
                {
                    "factura": "FP002",
                    "numero_factura": "FAC002",
                    "pagador": "Maria Garcia",
                    "vencimiento": "2012-10-31",
                    "total": 2000.00
                }
            ]
        },
        {
            "username": "23456789h",
            "plot": {
                "name": "Parcela Ejemplo 3",
                "coordinates": [[
                    [2.049752, 41.321370],
                    [2.052340, 41.322352],
                    [2.053241, 41.32118503],
                    [2.050672, 41.320052],
                    [2.049752, 41.321370]
                ]]
            },
            "caracteristicas": {
                "identificacion": "03-1",
                "parcela_catastral": "160909-003-005",
                "sup_total": 4.0000,
                "sup_regable": 3.8000,
                "num_olivos": 1800,
                "concesion": "Con concesión",
                "toma_agua": "Agr. 3",
                "suelo": "Suelo Arcilloso",
                "paraje": "Valle Central",
                "fecha_alta": "2010-08-20"
            },
            "usos_parcela": [
                {
                    "tipo_uso": "Agricultura",
                    "cultivo": "Olivar",
                    "superficie": 3.0,
                    "sistema_riego": "Goteo",
                    "estado": "Activo",
                    "fecha_alta": "2010-08-20",
                    "fecha_baja": None
                }
            ],
            "contadores_medidas": [
                {
                    "contador": "003005",
                    "fecha_alta": "2011-01-12",
                    "fecha_baja": None,
                    "lectura_max": 750000
                }
            ],
            "consumos": [
                {
                    "numero_factura": "FAC003",
                    "periodo_facturacion": "2013-11",
                    "volumen_medido": 35000,
                    "comentario": "Consumo de riego"
                }
            ],
            "datos_adicionales": [
                {
                    "tipo_dato": "Salinidad del agua",
                    "valor": "0.5"
                }
            ],
            "control_pagos": [
                {
                    "factura": "FP003",
                    "numero_factura": "FAC003",
                    "pagador": "Luis Fernandez",
                    "vencimiento": "2013-11-30",
                    "total": 3000.00
                }
            ]
        }
    ]

    for parcela_data in parcelas_data:
        try:
            user = User.objects.get(username=parcela_data["username"])

            plot, plot_created = create_plot(parcela_data["plot"])
            if plot_created:
                print(f"Plot '{plot.name}' added")

            plot.usuarios.add(user)  # Añadir usuario al plot

            caracteristicas_data = parcela_data["caracteristicas"]
            caracteristicas, created = CaracteristicasParcela.objects.get_or_create(plot=plot, **caracteristicas_data)
            if created:
                print(f'CaracteristicasParcela creada para el plot: {plot.name}')
            else:
                print(f'CaracteristicasParcela ya existente para el plot: {plot.name} - No se creó de nuevo')

            create_related_models(
                caracteristicas,
                parcela_data["usos_parcela"],
                parcela_data["contadores_medidas"],
                parcela_data["consumos"],
                parcela_data["datos_adicionales"],
                parcela_data["control_pagos"]
            )

        except User.DoesNotExist:
            print(f'Usuario {parcela_data["username"]} no encontrado.')
        except Exception as e:
            print(f'Error al procesar las parcelas para el usuario {parcela_data["username"]}: {e}')

def run():
    create_parcelas()
