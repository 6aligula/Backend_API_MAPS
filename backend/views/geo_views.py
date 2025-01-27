# geo_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from ..models import Location, Plot
from ..serializers import LocationSerializer, PlotSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def addPlot(request):
    serializer = PlotSerializer(data=request.data)
    print(f"datos del front {request.data}")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlot(request):
    if request.method == 'GET':
        user = request.user
        plots = Plot.objects.filter(usuarios=user)
        serializer = PlotSerializer(plots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def getLocations(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        print(serializer.data)
        return Response(serializer.data)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])  # Asegúrate de requerir autenticación si es necesario
def addLocation(request):
    serializer = LocationSerializer(data=request.data)
    print(f"datos del front", request.data)
    if serializer.is_valid():
        serializer.save()
        print(f"datos del back", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)