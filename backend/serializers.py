from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.gis.geos import Point
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Location, Plot, ContactMessage, Perfil
from .models import CaracteristicasParcela, UsoParcela, ContadoresMedidas, Consumos, DatosAdicionales, ControlPagos, ComunidadRegantes, Cultivo, FaseCultivo, RegistroDocumento, Peticion, Incidencia, Factura, LineaFactura

class LineaFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaFactura
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    lineas = LineaFacturaSerializer(many=True, read_only=True)
    pagado = serializers.SerializerMethodField()
    recargo_aplicado = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = '__all__'

    def get_pagado(self, obj):
        return obj.estado == 'Pagado'

    def get_recargo_aplicado(self, obj):
        return obj.recargo > 0

class IncidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidencia
        fields = '__all__'

class PeticionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peticion
        fields = '__all__'

class RegistroDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDocumento
        fields = '__all__'

class CultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultivo
        fields = '__all__'

class FaseCultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaseCultivo
        fields = '__all__'

class ComunidadRegantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComunidadRegantes
        fields = '__all__'

class PerfilSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    comunidades_regantes = ComunidadRegantesSerializer(many=True, read_only=True)  # Ajustado para ManyToMany

    class Meta:
        model = Perfil
        fields = '__all__'
    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)  # Añado esto para incluir el perfil en la respuesta
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'perfil']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class UsoParcelaSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    class Meta:
        model= UsoParcela
        fields= '__all__'
    
    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

class ContadoresMedidasSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    class Meta:
        model= ContadoresMedidas
        fields= '__all__'
    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

class ConsumosSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    class Meta:
        model= Consumos
        fields= '__all__'
    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

class DatosAdicionalesSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    class Meta:
        model= DatosAdicionales
        fields= '__all__'
    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

class ControlPagosSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    class Meta:
        model= ControlPagos
        fields= '__all__'
    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

'''
La estructura de la respuesta sigue el estándar GeoJSON, que es exactamente lo que se espera cuando se utilizan
serializadores de GeoDjango como GeoFeatureModelSerializer. Un FeatureCollection es una forma de agrupar múltiples
"features" (en este caso, ubicaciones con coordenadas geográficas) en un único objeto GeoJSON.
'''
class LocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Location
        geo_field = "coordinates"  # Asegura que este es el campo geoespacial en tu modelo
        fields = ('id', 'name', 'coordinates')

    def create(self, validated_data):
        print(f"dentro de create: {validated_data}")  # Ya tienes este
        
        # geojson_coordinates ya es un objeto Point
        geojson_coordinates = validated_data.pop('coordinates', None)
        
        if isinstance(geojson_coordinates, Point):
            # Si geojson_coordinates es una instancia de Point, puedes usarla directamente
            print(f"Usando Point directamente: {geojson_coordinates}")  # Debug: verificar el objeto Point
            
            # Crea y devuelve una nueva instancia de Location con el objeto Point
            return Location.objects.create(**validated_data, coordinates=geojson_coordinates)
        else:
            raise ValueError("Coordenadas inválidas o no proporcionadas")

class PlotSerializer(GeoFeatureModelSerializer):
    usuarios = UserSerializer(many=True, read_only=True)  # Incluye la relación usuarios

    class Meta:
        model = Plot
        geo_field = "bounds"
        fields = ('id', 'name', 'bounds', 'usuarios')

class CaracteristicasParcelaSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    plot = PlotSerializer(read_only=True)  # Incluye el serializer Plot para la relación

    class Meta:
        model = CaracteristicasParcela
        fields = '__all__'

    def get_isAdmin(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.is_staff
        return False

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'