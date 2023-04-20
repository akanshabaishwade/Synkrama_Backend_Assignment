from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


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
    


class BlogGetSerializer(serializers.Serializer):
    author_name = serializers.CharField(source="author.name")
    class Meta:
        model = Blog
        fields = ['author', 'author_name', 'title', 'body']



class BlogPostSerializer(serializers.Serializer):
    class Meta:
        model = Blog
        fields = ['author', 'title', 'body']