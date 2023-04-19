from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .serializer import *
from rest_framework import permissions
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics




class RegisterApi(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def loginApi(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        token, _ = Token.objects.get_or_create(user=username)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutApi(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_passwordApi(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.data.get('old_password')):
            return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogApi(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
