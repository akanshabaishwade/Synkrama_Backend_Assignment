from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.contrib.auth import logout, login
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse


class RegistrationView(APIView):
    def post(self, request):
        # get user input
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        name = request.data.get('name')

        # create new user
        user = User.objects.create_user(username=username, password=password, email=email,
                                        name=name)

        # return success message
        return Response({'message': 'User created successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutApi(request):
    logout(request)
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


@api_view(['POST'])
def change_passwordApi(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    new_password = request.data.get('new_password')
    if not new_password:
        return Response({'message': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_blog(request):
    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_blog(request):
    all_blog = Blog.objects.all().values()
    return Response(all_blog)
    # serializer = BlogGetSerializer(all_blog, many=True)
    # return Response(serializer.data)


@api_view(['GET'])
def get_single_blog(request, blog_id):
    blog = Blog.objects.filter(blog_id=blog_id).values()

    return Response(blog)


@api_view(['GET'])
def get_blogs_by_author(request, author):
    all_blog = Blog.objects.filter(author=author).values()
    return Response(all_blog)


class BlogUpdateApi(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogPostSerializer


def blog_delete(request, blog_id):
    blog = Blog.objects.get(blog_id=blog_id)
    blog.delete()
    message = {'message': 'Post deleted successfully.'}
    return JsonResponse(message)
