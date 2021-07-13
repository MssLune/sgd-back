from django.urls import path
from rest_framework import routers

from .api.viewset.calification_viewset import CalificationViewSet
from .api.viewset.scheduled_service_viewset import ScheduledServiceViewSet
from .api.viewset.service_viewset import ServiceViewSet
from .api.viewset.user_viewset import UserViewSet

app_name = 'public'
router = routers.DefaultRouter()
router.register('califications', CalificationViewSet)
router.register('scheduled_services', ScheduledServiceViewSet)
router.register('services', ServiceViewSet)
router.register('users', UserViewSet)

urlpatterns = [

]

urlpatterns += router.urls
