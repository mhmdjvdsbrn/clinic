from django.db import models
from django.contrib.auth.models import PermissionsMixin 
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import BaseUserManager as BUM 

class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseUserManager(BUM):
    def create_user(self, email, last_name, first_name , is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), is_admin=is_admin 
                            ,first_name=first_name, last_name=last_name)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email ,first_name="admin", last_name="", password=None):
        user = self.create_user(
            email=email,
            is_admin=True,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user

    

class BaseUser(BaseModel ,AbstractBaseUser ,PermissionsMixin):

    email = models.EmailField(verbose_name="email address", unique=True)
    full_name = models.CharField(max_length=35 ,null=True ,blank=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin