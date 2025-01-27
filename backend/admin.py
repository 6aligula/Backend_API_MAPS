from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Perfil, ContactMessage, Location, Plot, CaracteristicasParcela, 
    UsoParcela, ContadoresMedidas, Consumos, DatosAdicionales, 
    ControlPagos, ComunidadRegantes, Cultivo, FaseCultivo, 
    RegistroDocumento, Peticion, Incidencia, Factura, LineaFactura
)
from django.utils.translation import gettext_lazy as _
from leaflet.admin import LeafletGeoAdmin
# from .forms import PlotForm
from django.utils.html import format_html


class PlotAdmin(LeafletGeoAdmin):
    list_display = ('name',)
    readonly_fields = ('display_bounds',)

    def display_bounds(self, obj):
        return format_html("<pre>{}</pre>", obj.bounds)

    display_bounds.short_description = "Bounds (Read Only)"


class LineaFacturaInline(admin.TabularInline):
    model = LineaFactura
    extra = 1
    fields = ['concepto', 'unidades', 'precio_unitario', 'iva', 'total']
    readonly_fields = ['total']  # Asegúrate de que el total no se pueda editar directamente

class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'fecha_emision', 'total_facturado', 'estado']
    inlines = [LineaFacturaInline]
    readonly_fields = ['total_facturado']  # Opcional, para evitar edición directa

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total()  # Actualiza el total cada vez que se guardan las líneas

# Clase para manejar el modelo Perfil en la misma página del usuario
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'
    extra = 0  # No añadir nuevos perfiles vacíos por defecto

# Extender la administración del modelo User para incluir la información de Perfil
# fieldsets define la organización de campos en la página de edición de un usuario existente.
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    # Esto se muestra en la vista de lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Campos al crear un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

# Desregistrar la administración por defecto de User y registrar la nueva
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registrar el modelo Perfil si también quieres manejarlo de forma independiente
admin.site.register(Perfil)

# Registrar otros modelos
admin.site.register(ContactMessage)
admin.site.register(Location)
admin.site.register(Plot, PlotAdmin)
admin.site.register(CaracteristicasParcela)
admin.site.register(UsoParcela)
admin.site.register(ContadoresMedidas)
admin.site.register(Consumos)
admin.site.register(DatosAdicionales)
admin.site.register(ControlPagos)
admin.site.register(ComunidadRegantes)
admin.site.register(Cultivo)
admin.site.register(FaseCultivo)
admin.site.register(RegistroDocumento)
admin.site.register(Peticion)
admin.site.register(Incidencia)
admin.site.register(Factura, FacturaAdmin)
