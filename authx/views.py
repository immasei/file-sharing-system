from django.shortcuts import render

# Create your views here.
from rest_framework import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *

# login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# register 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens using RefreshToken
        token = CustomTokenObtainPairSerializer(data={
            'email': request.data['email'],
            'password': request.data['password']
        })
        token.is_valid(raise_exception=True)
        token = token.validated_data  

        response = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'avatar': user.avatar,
            'quota_limit': user.quota_limit,
            'quota_used': user.quota_used,
            'refresh': token['refresh'],
            'access': token['access'],
        }

        return Response(response, status=status.HTTP_201_CREATED)

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)