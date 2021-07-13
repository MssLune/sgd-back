"""sgd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from .token import CustomObtainPairView

urlpatterns = [
    # authentication
    path('v1/auth/login/', CustomObtainPairView.as_view(), name='token-obtain'),
    path('v1/auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('v1/auth/verify/', TokenVerifyView.as_view(), name='token-verify'),

    # app urls
    path('v1/', include('public.urls')),

    # schema api
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
    ]
