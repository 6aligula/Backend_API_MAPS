from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Peticion
from ..serializers import PeticionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_peticion(request):
    user = request.user
    data = request.data.copy()
    data['usuario'] = user.id
    
    serializer = PeticionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_peticiones(request):
    user = request.user
    peticiones = Peticion.objects.filter(usuario=user)
    serializer = PeticionSerializer(peticiones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
