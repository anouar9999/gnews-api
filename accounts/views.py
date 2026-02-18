from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .serializers import SetupAdminSerializer, LoginSerializer, UserSerializer, CreateUserSerializer, UpdateUserSerializer
from .permissions import IsAdmin

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Admin-only CRUD for editor/viewer accounts."""
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email']

    def get_queryset(self):
        return User.objects.exclude(user_type='admin').order_by('-date_joined')

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action in ('update', 'partial_update'):
            return UpdateUserSerializer
        return UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def setup_admin(request):
    """Create the initial admin user. Only works if no admin-type user exists."""
    if User.objects.filter(user_type='admin').exists():
        return Response(
            {'error': 'An admin user already exists.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = SetupAdminSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        user_type='admin',
        is_staff=True,
        is_superuser=True,
    )

    return Response(
        UserSerializer(user).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Authenticate an admin user and return JWT tokens."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
    )

    if user is None:
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        },
    })
