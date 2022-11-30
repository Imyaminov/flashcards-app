from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            'error': 'This email is already exists!'
        }
    )
    username = models.CharField(
        max_length=256,
        unique=True,
        error_messages={
            'error': 'This username is already exists'
        }
    )
    password = models.CharField(
        max_length=16,
        validators=[MinLengthValidator(8)],
        error_messages={
            'error': 'Password must contain at least 8 characters!'
        }
    )
    avatar = models.ImageField(default='default.jpg', upload_to='profile/')

    def __str__(self):
        return self.username


