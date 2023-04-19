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
        extra_kwargs = {'password': {'write_only': True}}



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
    


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return value

    def save(self):
        username = self.validated_data.get('username')
        user = User.objects.get(username=username)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user



class BlogSerializer(serializers.Serializer):
    class Meta:
        model = Blog
        fields = "__all__"
