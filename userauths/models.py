from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']




    def __str__(self):
        return self.username
