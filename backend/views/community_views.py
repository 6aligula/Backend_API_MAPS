
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from backend.serializers import ComunidadRegantesSerializer, Perfil
from backend.models import ComunidadRegantes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCommunityProfile(request):
    try:
        perfil = Perfil.objects.get(usuario=request.user)
        comunidades = perfil.comunidades_regantes.all()
        serializer = ComunidadRegantesSerializer(comunidades, many=True)
        return Response(serializer.data)
    except Perfil.DoesNotExist:
        return Response(
            {"detail": "Perfil no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCommunity(request):
    try:
        # Supongamos que request.data contiene una lista de comunidades actualizadas
        comunidades_data = request.data
        updated_comunidades = []

        for comunidad_data in comunidades_data:
            comunidad_id = comunidad_data.get('id')
            if comunidad_id:
                try:
                    comunidad = ComunidadRegantes.objects.get(id=comunidad_id)
                    serializer = ComunidadRegantesSerializer(comunidad, data=comunidad_data)
                    if serializer.is_valid():
                        serializer.save()
                        updated_comunidades.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except ComunidadRegantes.DoesNotExist:
                    return Response(
                        {"detail": f"Comunidad con id {comunidad_id} no encontrada."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {"detail": "ID de la comunidad es requerido."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(updated_comunidades, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )