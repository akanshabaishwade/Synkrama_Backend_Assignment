from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'username', 'name', 'date_of_birth',
                  'address', 'phone_number', 'updated_at']


# class RegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('username','password', 'name', 'date_of_birth',
#                     'address', 'phone_number',)

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             name=validated_data['name'],
#             email=validated_data['email'],
#             date_of_birth=validated_data['date_of_birth'],

#         )
#         return user

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','password', 'name','email', 'date_of_birth',
                    'address', 'phone_number',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            email=validated_data['email'],
            date_of_birth=validated_data['date_of_birth'],
        )
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email address is already registered.')
        return value
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.')
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid login credentials.')

        data['user'] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return value


class BlogSerializer(serializers.Serializer):
    class Meta:
        model = Blog
        fields = "__all__"
