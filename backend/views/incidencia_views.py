from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Incidencia
from ..serializers import IncidenciaSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_incidencia(request):
    user = request.user
    data = request.data.copy()
    data['usuario'] = user.id
    
    serializer = IncidenciaSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_incidencias(request):
    user = request.user
    incidencias = Incidencia.objects.filter(usuario=user)
    serializer = IncidenciaSerializer(incidencias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
