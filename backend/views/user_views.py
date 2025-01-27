
from backend.models import Perfil
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from backend.serializers import UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str



User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')  # username se asume como DNI
        password = attrs.get('password')
        print(username, password)

        try:
            user = authenticate(username=username, password=password)
            if not user:
                raise AuthenticationFailed('Usuario no encontrado o contraseña incorrecta.')

            data = super().validate(attrs)  # Llama a la validación base que genera los tokens
            serializer = UserSerializerWithToken(user).data
            for k, v in serializer.items():
                data[k] = v

            print(f'Inicio de sesión exitoso para el usuario: {username}')
            return data
        except AuthenticationFailed as e:
            print(f'Intento de inicio de sesión fallido para el usuario: {username}')
            raise e 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    email = (data['email']).strip().lower()
    name = (data['name']).strip()
    password = (data['password']).strip()

    try:
        user = User.objects.create(
            first_name=name,
            username=email,
            email=email,
            password=make_password(password)
        )
        serializer = UserSerializerWithToken(user, many=False)
        print(f'Usuario registrado con éxito: {email}.')
        return Response(serializer.data)
    except Exception as e:
        print(f'Error al registrar usuario: {str(e)}.')
        message = {'detail': 'La información proporcionada no es válida, revisa el formato de tu correo'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


def update_attribute_if_provided(instance, attribute, value):
    """
    Actualiza un atributo de una instancia si el valor proporcionado no está vacío.
    
    :param instance: La instancia a actualizar.
    :param attribute: El nombre del atributo a actualizar.
    :param value: El valor nuevo para el atributo.
    """
    if value is not None and value != '':
        setattr(instance, attribute, value)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUserProfile(request):
    user = request.user
    data = request.data

    # Actualiza atributos del modelo User
    update_attribute_if_provided(user, 'first_name', data.get('name'))
    update_attribute_if_provided(user, 'email', data.get('email'))
    if 'password' in data and data['password']:
        user.password = make_password(data['password'])
    user.save()

    # Obtener o crear el perfil si no existe
    perfil, created = Perfil.objects.get_or_create(usuario=user)
    
    # Campos del perfil que pueden actualizarse
    profile_fields = [
        'cif', 'direccion', 'localidad', 'codigo_postal', 'telefono_fijo', 'telefono_movil',
        'email_alternativo', 'nombre_entidad', 'numero_banco', 'numero_sucursal',
        'digito_control', 'numero_cuenta', 'cargo', 'telefono_contacto', 'email_contacto', 'telefono_movil_contacto'
    ]
    # Actualiza atributos del modelo Perfil
    for field in profile_fields:
        update_attribute_if_provided(perfil, field, data.get(field))
    perfil.save()

    # Vuelve a generar el serializer para reflejar los cambios
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

# Funcion para recibir correo y enviar correo de recuperacion
@api_view(['POST'])
def forgotPassword(request):
    email = request.data['email']
    # No es necesario buscar si el usuario existe antes de enviar la respuesta.
    
    subject = 'Restablecimiento de Contraseña'
    message = ('Si tienes una cuenta en nuestro sitio, te hemos enviado un correo electrónico '
               'con instrucciones para restablecer tu contraseña. Por favor revisa tu correo '
               'electrónico, incluyendo la carpeta de spam.')
    
    try:
        user = User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_str(user.pk).encode())
        reset_url = f'http://localhost:3000/reset-password/{uid}/{token}'
        
        # Preparar el mensaje de correo electrónico.
        email_body = f'Hola {user.username},\n\nPor favor, haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}\n\nSi tú no solicitaste este cambio, ignora este correo y tu contraseña se mantendrá igual.'
        
        # Enviar correo electrónico.
        send_mail(
            subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
    except User.DoesNotExist:
        # Incluso si el usuario no existe, no revelamos esta información.
        print("Usuario no encontrado.")
        pass
    except Exception as e:
        # Aquí puedes querer logear el error para propósitos de debugging,
        # pero no le devuelvas al usuario detalles sobre el error.
        print("Error al enviar correo de recuperación de contraseña:", e)
        pass
    
    # Siempre devolvemos la misma respuesta al usuario.
    return Response({'message': message}, status=status.HTTP_200_OK)

@api_view(['POST'])
def resetPassword(request, uidb64, token):
    try:
        # Decodifica el uidb64 para obtener el ID del usuario
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)

        # Verificar si el token es válido
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'error': 'El token de restablecimiento no es válido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        # Recibir la nueva contraseña del cuerpo de la solicitud
        password = request.data.get('password')
        if not password:
            return Response({'error': 'No se ha proporcionado ninguna contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

        # Establecer la nueva contraseña
        user.set_password(password)
        user.save()

        return Response({'success': 'Contraseña restablecida correctamente.'}, status=status.HTTP_200_OK)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Operación no válida.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)