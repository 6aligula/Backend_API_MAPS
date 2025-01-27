from backend.models import CaracteristicasParcela, Consumos, ContadoresMedidas, ControlPagos, DatosAdicionales, UsoParcela
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from backend.serializers import CaracteristicasParcelaSerializer, ConsumosSerializer, ContadoresMedidasSerializer, ControlPagosSerializer, DatosAdicionalesSerializer, UsoParcelaSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def caracteristicas_parcela_list(request):
    if request.method == 'GET':
        parcelas = CaracteristicasParcela.objects.filter(plot__usuarios=request.user)
        serializer = CaracteristicasParcelaSerializer(parcelas, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CaracteristicasParcelaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def usos_parcela_list(request):
    if request.method == 'GET':
        usos = UsoParcela.objects.filter(parcela__plot__usuarios=request.user)
        serializer = UsoParcelaSerializer(usos, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsoParcelaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contadores_medidas_list(request):
    if request.method == 'GET':
        contadores = ContadoresMedidas.objects.filter(parcela__plot__usuarios=request.user)
        serializer = ContadoresMedidasSerializer(contadores, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ContadoresMedidasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def consumos_list(request):
    if request.method == 'GET':
        consumos = Consumos.objects.filter(parcela__plot__usuarios=request.user)
        serializer = ConsumosSerializer(consumos, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ConsumosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def datos_adicionales_list(request):
    if request.method == 'GET':
        datos = DatosAdicionales.objects.filter(parcela__plot__usuarios=request.user)
        serializer = DatosAdicionalesSerializer(datos, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DatosAdicionalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def control_pagos_list(request):
    if request.method == 'GET':
        pagos = ControlPagos.objects.filter(parcela__plot__usuarios=request.user)
        serializer = ControlPagosSerializer(pagos, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ControlPagosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
