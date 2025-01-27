from django.db import models
from django.contrib.gis.db.models import PointField, PolygonField
from django.contrib.auth.models import User
from decimal import Decimal

class Incidencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incidencias')
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

    def __str__(self):
        return f"{self.usuario.username} - {self.mensaje[:20]}"

class Peticion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='peticiones')
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Petición'
        verbose_name_plural = 'Peticiones'

    def __str__(self):
        return f"{self.usuario.username} - {self.mensaje[:20]}"

class RegistroDocumento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_documentos')
    numero_documento = models.CharField(max_length=100)
    fecha = models.DateField()
    asunto = models.CharField(max_length=255)
    localizacion = models.CharField(max_length=255)
    dirig = models.CharField(max_length=255)
    ruta_archivo = models.CharField(max_length=255, blank=True, null=True)  # Este campo es opcional, se puede quitar si no es necesario
    observaciones = models.TextField(blank=True, null=True)
    entrada = models.BooleanField(default=True)
    salida = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Registro de Documento'
        verbose_name_plural = 'Registros de Documentos'

    def __str__(self):
        return f"{self.numero_documento} - {self.asunto}"

class Cultivo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class FaseCultivo(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='fases_cultivo')
    fase = models.CharField(max_length=100)  # Fase inicial, media, final
    kc = models.DecimalField(max_digits=4, decimal_places=2)
    nap = models.IntegerField()
    prof_rad = models.DecimalField(max_digits=4, decimal_places=2)
    das_inicio = models.IntegerField()  # Días después de la siembra en que inicia la fase
    porcentaje_almacen = models.DecimalField(max_digits=5, decimal_places=2)  # % de pérdida o eficiencia de almacenamiento

    def __str__(self):
        return f"{self.cultivo.nombre} - {self.fase}"

class Plot(models.Model):
    name = models.CharField(max_length=255)
    bounds = PolygonField()  # Usamos un PolygonField para almacenar los límites de la parcela
    usuarios = models.ManyToManyField(User, related_name='plots')  # Relación muchos a muchos con usuarios

    def __str__(self):
        return self.name
   
class CaracteristicasParcela(models.Model):
    plot = models.OneToOneField(Plot, on_delete=models.CASCADE, related_name='caracteristicas', default=1)  # Relación uno a uno con Plot
    identificacion = models.CharField(max_length=20)
    parcela_catastral = models.CharField(max_length=50)
    sup_total = models.DecimalField(max_digits=10, decimal_places=4)
    sup_regable = models.DecimalField(max_digits=10, decimal_places=4)
    num_olivos = models.IntegerField()
    concesion = models.CharField(max_length=100)
    toma_agua = models.CharField(max_length=100)
    suelo = models.CharField(max_length=100)
    paraje = models.CharField(max_length=100)
    fecha_alta = models.DateField()

    def __str__(self):
        return self.identificacion
    
def get_default_parcela():
    default_parcela = CaracteristicasParcela.objects.first()
    if default_parcela:
        return default_parcela.id
    else:
        # Crear una instancia predeterminada si no existe
        default_parcela = CaracteristicasParcela.objects.create(
            usuario=User.objects.first(),  # Asumiendo que hay al menos un usuario
            identificacion='default',
            parcela_catastral='default',
            sup_total=0,
            sup_regable=0,
            num_olivos=0,
            concesion='default',
            toma_agua='default',
            suelo='default',
            paraje='default',
            fecha_alta='2000-01-01'
        )
        return default_parcela.id

class UsoParcela(models.Model):
    parcela = models.ForeignKey(CaracteristicasParcela, on_delete=models.CASCADE, related_name='usos_parcela', default=get_default_parcela)
    tipo_uso = models.CharField(max_length=100)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='usos_parcela')
    superficie = models.DecimalField(max_digits=10, decimal_places=4)
    sistema_riego = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_uso} - {self.cultivo}"

class ContadoresMedidas(models.Model):
    parcela = models.ForeignKey(CaracteristicasParcela, on_delete=models.CASCADE, related_name='contadores_medidas')
    contador = models.CharField(max_length=20)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(blank=True, null=True)
    lectura_max = models.IntegerField()

    def __str__(self):
        return self.contador

class Consumos(models.Model):
    parcela = models.ForeignKey(CaracteristicasParcela, on_delete=models.CASCADE, related_name='consumos')
    numero_factura = models.CharField(max_length=50)
    periodo_facturacion = models.CharField(max_length=50)
    volumen_medido = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.numero_factura} - {self.periodo_facturacion}"

class DatosAdicionales(models.Model):
    parcela = models.ForeignKey(CaracteristicasParcela, on_delete=models.CASCADE, related_name='datos_adicionales')
    tipo_dato = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo_dato} - {self.valor}"

class ControlPagos(models.Model):
    parcela = models.ForeignKey(CaracteristicasParcela, on_delete=models.CASCADE, related_name='control_pagos')
    factura = models.CharField(max_length=50)
    numero_factura = models.CharField(max_length=50)
    pagador = models.CharField(max_length=100)
    vencimiento = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.factura} - {self.total} EUR"
    
class ComunidadRegantes(models.Model):
    nombre = models.CharField(max_length=255,  unique=True)
    cif = models.CharField(max_length=9)
    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    telefono_fijo = models.CharField(max_length=15, blank=True, null=True)
    telefono_movil = models.CharField(max_length=15, blank=True, null=True)
    email_alternativo = models.EmailField(blank=True, null=True)
    
    # Datos bancarios
    nombre_entidad = models.CharField(max_length=100)
    numero_banco = models.CharField(max_length=4)
    numero_sucursal = models.CharField(max_length=4)
    digito_control = models.CharField(max_length=2)
    numero_cuenta = models.CharField(max_length=10)
    
    # Información de cargos en la comunidad
    cargo = models.CharField(max_length=255, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    telefono_movil_contacto = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Comunidad de Regantes'
        verbose_name_plural = 'Comunidades de Regantes'

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    comunidades_regantes = models.ManyToManyField(ComunidadRegantes, related_name="miembros")
    cif = models.CharField(max_length=9)
    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    telefono_fijo = models.CharField(max_length=15, blank=True, null=True)
    telefono_movil = models.CharField(max_length=15, blank=True, null=True)
    email_alternativo = models.EmailField(blank=True, null=True)
    
    # Datos bancarios
    nombre_entidad = models.CharField(max_length=100)
    numero_banco = models.CharField(max_length=4)
    numero_sucursal = models.CharField(max_length=4)
    digito_control = models.CharField(max_length=2)
    numero_cuenta = models.CharField(max_length=10)
    
    # Información de cargos en la comunidad
    cargo = models.CharField(max_length=255, blank=True, null=True) # Puedes querer usar un modelo separado para los cargos si hay múltiples cargos por usuario.
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    telefono_movil_contacto = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f"{self.usuario.username} - {self.cif}"


class Location(models.Model):
    name = models.CharField(max_length=255)
    coordinates = PointField()
    
    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Factura(models.Model):
    parcela = models.ForeignKey(CaracteristicasParcela, on_delete=models.CASCADE, related_name='facturas')
    numero_factura = models.IntegerField(unique=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    recargo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_facturado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=100, choices=[('Pagado', 'Pagado'), ('Pendiente', 'Pendiente'), ('Vencido', 'Vencido')])
    fecha_pago = models.DateField(null=True, blank=True)  # Agregar este campo si no existe

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def save(self, *args, **kwargs):
        if not self.id:  # Si es una nueva instancia, asigna el próximo número de factura
            max_number = Factura.objects.all().aggregate(models.Max('numero_factura'))['numero_factura__max']
            self.numero_factura = (max_number or 0) + 1

        super().save(*args, **kwargs)  # Asegúrate de llamar al método save() del padre primero

    def update_total(self):
        self.subtotal = sum(linea.total for linea in self.lineas.all())
        self.total_facturado = self.subtotal + self.recargo
        self.save()  # Guarda los cambios en la base de datos

    def __str__(self):
        return f"{self.numero_factura} - {self.total_facturado} EUR"


class LineaFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='lineas')
    concepto = models.CharField(max_length=255)
    unidades = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.IntegerField(choices=[(10, '10%'), (21, '21%'), (0, '0%')])
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        iva_as_decimal = Decimal(str(self.iva))
        self.total = self.unidades * self.precio_unitario * (Decimal('1.0') + iva_as_decimal / Decimal('100'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.concepto} - Total: {self.total}"