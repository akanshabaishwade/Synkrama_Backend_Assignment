from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "name", "updated_at")


admin.site.register(User, UserAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ("blog_id", "author", "title", "updated_at")


admin.site.register(Blog, BlogAdmin)
