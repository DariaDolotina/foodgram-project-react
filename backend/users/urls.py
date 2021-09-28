from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]