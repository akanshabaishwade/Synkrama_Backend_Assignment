from django.urls import path
from .api import *



urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutApi, name='logout'),
    path('change_password/<str:username>/', change_passwordApi, name='change_password'),
    path('api/posts/get/', get_all_blog, name='get_all_blog'),
    path('api/post/blog/', create_blog, name='create_blog'),
    path('api/blog/blogid/<int:blog_id>/', get_single_blog, name='get_single_blog'),
    path('api/blog/author/<str:author>/', get_blogs_by_author, name='get_blogs_by_author'),
    path('blog/update/<int:blog_id>/', BlogUpdateApi.as_view(), name='blog_update'),
    path('blog/delete/<int:blog_id>/', blog_delete, name='blog_delete'),




]
