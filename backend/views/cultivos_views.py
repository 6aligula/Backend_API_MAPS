from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Cultivo, FaseCultivo
from ..serializers import CultivoSerializer, FaseCultivoSerializer, CaracteristicasParcela

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cultivo_list(request):
    user = request.user
    parcelas = CaracteristicasParcela.objects.filter(plot__usuarios=user)
    cultivos = Cultivo.objects.filter(usos_parcela__parcela__in=parcelas).distinct()
    serializer = CultivoSerializer(cultivos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cultivo_detail(request, pk):
    user = request.user
    try:
        parcelas = CaracteristicasParcela.objects.filter(plot__usuarios=user)
        cultivo = Cultivo.objects.get(pk=pk, usos_parcela__parcela__in=parcelas)
    except Cultivo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CultivoSerializer(cultivo)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fase_cultivo_detail(request, pk):
    user = request.user
    try:
        parcelas = CaracteristicasParcela.objects.filter(plot__usuarios=user)
        fase_cultivo = FaseCultivo.objects.get(pk=pk, cultivo__usos_parcela__parcela__in=parcelas)
    except FaseCultivo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FaseCultivoSerializer(fase_cultivo)
    return Response(serializer.data, status=status.HTTP_200_OK)

