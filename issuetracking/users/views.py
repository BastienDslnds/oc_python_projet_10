from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.permissions import AllowAny

from users.models import User
from .serializers import SignupSerializer, UserSerializer


@api_view(['POST'])
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


# class SignupAPIView(APIView):

#     permission_classes = (AllowAny,)

#     def post(self, request):
#         data = request.data
#         serializer = SignupSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes(
    [
        AllowAny,
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


# @api_view(['POST'])
# @permission_classes(
#     [
#         AllowAny,
#     ]
# )
# def login(request):
#     try:
#         email = request.data['email']
#         password = request.data['password']
#         user = User.objects.get(email=email, password=password)
#         if user:
#             try:
#                 payload = jwt_payload_handler(user)
#                 token = jwt.encode(payload, settings.SECRET_KEY)
#                 user_details = {}
#                 user_details['name'] = "%s %s" % (
#                     user.first_name,
#                     user.last_name,
#                 )
#                 user_details['token'] = token
#                 user_logged_in.send(
#                     sender=user.__class__, request=request, user=user
#                 )
#                 return Response(user_details, status=status.HTTP_200_OK)
#             except Exception as e:
#                 raise e
#         else:
#             res = {
#                 'error': 'can not authenticate with the given credentials or the account has been deactivated'
#             }
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {'error': 'please provide a email and a password'}
#         return Response(res)
