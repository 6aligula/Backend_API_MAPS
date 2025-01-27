# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Detailed documentation of all endpoints",
        terms_of_service="https://www.yourcompany.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourcompany.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('backend.urls.user_urls')),
    path('api/geo/', include('backend.urls.geo_urls')),
    path('api/contact/', include('backend.urls.contact_urls')),
    path('api/parcelas/', include('backend.urls.parcelas_urls')),
    path('api/community/', include('backend.urls.community_urls')),
    path('api/inventario/', include('backend.urls.cultivos_urls')),
    path('api/documentos/', include('backend.urls.documentos_urls')),
    path('api/peticiones/', include('backend.urls.peticiones_urls')), 
    path('api/incidencias/', include('backend.urls.incidencia_urls')), 
    path('api/consumos/', include('backend.urls.consumos_urls')), 
    path('api/facturas/', include('backend.urls.facturas_urls')), 
    # swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
