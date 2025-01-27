from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os

from ..models import RegistroDocumento
from ..serializers import RegistroDocumentoSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_documentos(request):
    user = request.user
    documentos = RegistroDocumento.objects.filter(usuario=user)
    serializer = RegistroDocumentoSerializer(documentos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def crear_documento(request):
    user = request.user
    data = request.data.copy()  # Hacer una copia del QueryDict
    data['usuario'] = user.id  # Añadir el usuario al payload

    # Manejo de archivos
    archivo = request.FILES.get('ruta_archivo')
    if archivo:
        archivo_path = os.path.join('documentos', archivo.name)
        full_path = os.path.join('media', archivo_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb+') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)
        data['ruta_archivo'] = archivo_path

    serializer = RegistroDocumentoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_documento(request, pk):
    try:
        documento = RegistroDocumento.objects.get(pk=pk, usuario=request.user)
        serializer = RegistroDocumentoSerializer(documento)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except RegistroDocumento.DoesNotExist:
        return Response({'detail': 'Documento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
