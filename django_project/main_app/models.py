from django.db import models
from datetime import timezone
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    updated_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.username

class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User,
        to_field="username",
        related_name="username_author",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=30, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.author}"
