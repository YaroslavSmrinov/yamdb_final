from rest_framework import filters, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from users.permissions import IsAdmin
from users.serializers import (TokenObtainSerializer, User, UserSerializer,
                               UserSignUpSerializer)
from users.tokens import account_activation_token


@api_view(['POST'])
def user_sign_up(request):
    serializer = UserSignUpSerializer(data=request.data)

    existing_user = User.objects.filter(
        username=request.data.get('username')
    ).first()
    if existing_user and existing_user.email == request.data.get('email'):
        return Response(request.data, status=status.HTTP_200_OK)

    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    password = User.objects.make_random_password()
    user.set_password(password)
    user.save(update_fields=['password'])
    subject = 'Activate Your YAMDB Account'
    message = (
        f'Привет {user.username},\n'
        + 'Спасибо за использование YAMDB.\n'
        + f'Твой код подтверждения {account_activation_token.make_token(user)}'
    )
    user.email_user(subject, message)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenViewBase):
    serializer_class = TokenObtainSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdmin)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path='me',
    )
    def current_user(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('role', None)
        serializer.update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
