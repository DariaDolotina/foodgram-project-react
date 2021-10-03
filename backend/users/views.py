from rest_framework.permissions import AllowAny
from djoser.views import UserViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(UserViewSet):
    serializer_class = UserSerializer(many=True)
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
