from django.db import models

# Create your models here.

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manayers import Usermanayer


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    gmail = models.EmailField()
    nombre = models.CharField(max_length=20, blank=True)
    apellido = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = Usermanayer()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gmail']    
   
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def _str_(self) -> str:

        return str(self.id) +'--'+ self.username