from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import CaracteristicasParcela, Consumos
from ..serializers import ConsumosSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_consumos(request):
    user = request.user
    parcelas = CaracteristicasParcela.objects.filter(plot__usuarios=user)
    consumos = Consumos.objects.filter(parcela__in=parcelas)
    serializer = ConsumosSerializer(consumos, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
