from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response 


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                raise AuthenticationFailed('User is deactivated')

            data = {}
            refresh = self.get_token(user)

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data
        else:
            raise AuthenticationFailed('No active account found with the given credentials')

class RegisterSerializer(serializers.ModelSerializer):
    # write only ~input
    # read only  ~excluded from request body and input validation
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, min_length=2, max_length=30)
    password = serializers.CharField(write_only=True, min_length=2, required=True)  # validators=[validate_password]
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    avatar = serializers.URLField(read_only=True, allow_null=True)
    quota_limit = serializers.DecimalField(decimal_places=1, max_digits=4, read_only=True)
    quota_used = serializers.DecimalField(decimal_places=1, max_digits=4, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'avatar', 'quota_limit', 'quota_used')

    def create(self, validated_data):
        # signup
        if not validated_data.get('username'):
            raise serializers.ValidationError("Username is required.")

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
