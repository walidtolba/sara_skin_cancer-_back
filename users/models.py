from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
import os


class User(AbstractBaseUser, PermissionsMixin):
    def get_upload_to(self, filename):
        return os.path.join('images', 'profile_pictures', str(self.pk), filename)
    genders = (('female', 'Female'), ('male', 'Male'))
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=16, choices=genders, null=False, blank=False)
    picture = models.ImageField(upload_to=get_upload_to, default='images/profile_pictures/default_profile_picture.jpg')
    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class VerificationCode(models.Model):
    code = models.CharField(max_length=5, null=False, blank=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    
    def __str__(self):
        return self.user.email