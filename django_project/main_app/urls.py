from django.urls import path
from .api import *



urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', logoutApi, name='logout'),
    path('change_password/', change_passwordApi, name='change_password'),
    path('api/posts/', BlogApi.as_view({'get': 'list', 'post': 'create'})),
    path('login/', LoginView.as_view())

]
