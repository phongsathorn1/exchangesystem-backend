from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer, UserViewSerializer


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                birthday=serializer.validated_data['birthday'],
                gender=serializer.validated_data['gender'],
                phone=serializer.validated_data['phone']
            )

            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserViewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)
