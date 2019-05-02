from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer, UserViewSerializer
from rest_framework_jwt.settings import api_settings


@api_view(['POST'])
@permission_classes((~IsAuthenticated,))
def create_user(request, format=None):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            phone=serializer.validated_data['phone']
        )

        if 'birthday' in serializer.validated_data:
            user.birthday = serializer.validated_data['birthday']

        if 'gender' in serializer.validated_data:
            user.gender = serializer.validated_data['gender']

        user.save()

        if user:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            print(token)

            context = {
                **serializer.data,
                'token': token
            }

            return Response(context, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserViewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_me(request, format=None):
    user = User.objects.get(pk=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def patch_me(request, format=None):
    user = User.objects.get(pk=request.user.id)
    serializer = UserSerializer(data=request.data)
    if user:
        user.email = serializer.validated_data['email']
        user.first_name = serializer.validated_data['first_name']
        user.last_name = serializer.validated_data['last_name']
        user.birthday = serializer.validated_data['birthday']
        user.gender = serializer.validated_data['gender']
        user.phone = serializer.validated_data['phone']
        user.picture = serializer.validated_data['picture']
        user.save()

        return Response(serializer.data, status.HTTP_200_OK)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def check_phone(request, format=None):
    if request.method == 'GET':
        phone_number = request.GET.get('phone')

    if request.method == 'POST':
        phone_number = request.POST.get('phone')

    if not phone_number:
        context = {
            'message': 'NO_PHONE_ENTER'
        }
        return Response(context, status.HTTP_400_BAD_REQUEST)

    phone = User.objects.filter(phone=phone_number).exists()
    if phone:
        context = {
            'message': 'PHONE_NOT_AVALIABLE'
        }
        return Response(context, status.HTTP_400_BAD_REQUEST)

    context = {
        'message': 'PHONE_AVALIABLE'
    }
    return Response(context, status.HTTP_200_OK)
