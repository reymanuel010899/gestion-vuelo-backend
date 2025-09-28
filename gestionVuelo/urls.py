from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Mi API",
        default_version='v1',
        description="Descripción de mi API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@miapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls', namespace='users')),
    path('gestion/', include('apps.gestion.urls', namespace='gestion'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)