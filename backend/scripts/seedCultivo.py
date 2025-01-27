from backend.models import Cultivo, FaseCultivo

def run():
    cultivos_data = [
        {"nombre": "Algodón"},
        {"nombre": "Maíz"},
        {"nombre": "Patata temprana"},
        {"nombre": "Girasol"},
        {"nombre": "Trigo"},
        {"nombre": "Ajo"},
        {"nombre": "Olivar"},
    ]

    for cultivo_data in cultivos_data:
        cultivo, created = Cultivo.objects.get_or_create(**cultivo_data)
        if created:
            print(f"Cultivo '{cultivo.nombre}' creado.")
        else:
            print(f"Cultivo '{cultivo.nombre}' ya existe.")

    fases_cultivo_data = [
        {"cultivo": "Algodón", "fase": "Inicial", "kc": 0.30, "nap": 60, "prof_rad": 0.40, "das_inicio": 10, "porcentaje_almacen": 5.0},
        {"cultivo": "Maíz", "fase": "Media", "kc": 1.20, "nap": 90, "prof_rad": 0.60, "das_inicio": 20, "porcentaje_almacen": 10.0},
        {"cultivo": "Patata temprana", "fase": "Final", "kc": 0.80, "nap": 120, "prof_rad": 0.80, "das_inicio": 30, "porcentaje_almacen": 15.0},
        {"cultivo": "Girasol", "fase": "Inicial", "kc": 0.35, "nap": 70, "prof_rad": 0.45, "das_inicio": 15, "porcentaje_almacen": 6.0},
        {"cultivo": "Trigo", "fase": "Media", "kc": 1.25, "nap": 85, "prof_rad": 0.55, "das_inicio": 25, "porcentaje_almacen": 12.0},
        {"cultivo": "Ajo", "fase": "Final", "kc": 0.75, "nap": 110, "prof_rad": 0.70, "das_inicio": 28, "porcentaje_almacen": 14.0},
        {"cultivo": "Olivar", "fase": "Inicial", "kc": 0.40, "nap": 65, "prof_rad": 0.50, "das_inicio": 18, "porcentaje_almacen": 8.0},
    ]

    for fase_data in fases_cultivo_data:
        cultivo = Cultivo.objects.get(nombre=fase_data["cultivo"])
        fase_data["cultivo"] = cultivo
        fase_cultivo, created = FaseCultivo.objects.get_or_create(**fase_data)
        if created:
            print(f"Fase de cultivo '{fase_cultivo.fase}' para '{cultivo.nombre}' creada.")
        else:
            print(f"Fase de cultivo '{fase_cultivo.fase}' para '{cultivo.nombre}' ya existe.")
