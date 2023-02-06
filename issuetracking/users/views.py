from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from .serializers import SignupSerializer, UserSerializer


@api_view(['POST'])
@permission_classes(
    [
        AllowAny,
    ]
)
def signup(request):
    data = request.data
    print(data)
    serializer = SignupSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
            )
            user.save()
            return Response(
                {'message': 'User Created Successfully'},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'message': 'User Already Exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def login(request):
    email = request.data['email']
    password = request.data['password']
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.check_password(password):
            return Response(
                UserSerializer(instance=user).data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Invalid Password'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {'message': 'User Does Not Exist'},
            status=status.HTTP_400_BAD_REQUEST,
        )
