from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)

from uuid import uuid4

import os

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError()
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

def get_upload_path(instance, filename):
    return os.path.join('images', 'avatars', str(instance.pk), filename)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

class EmailConfirmationToken(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)