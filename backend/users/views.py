from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer(many=True)
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        user = request.user

        data = {
            'user': user.id,
            'author': author_id
        }
        serializer = FollowSerializer(data=data, context={'request': request})

        if not serializer.is_valid():
            Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        user = request.user
        author = get_object_or_404(CustomUser, id=author_id)
        obj = get_object_or_404(Follow, user=user, author=author)
        obj.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )