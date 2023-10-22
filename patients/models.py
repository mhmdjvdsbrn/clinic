from django.db import models
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
    def create_user(self, national_code,first_name, last_name, age=None , description=None, is_admin=False,password=None ):
        if not national_code:
            raise ValueError("Users must have an national_code address")

        user = self.model(national_code=national_code, is_admin=is_admin ,first_name=first_name
                        , last_name=last_name, age=age, description=description)


        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
        print()
        print(password)
        user.full_clean()
        user.save(using=self._db)
        return user
    def create_superuser(self, national_code ,first_name="admin",last_name="fuck" 
                        , password=None):
        user = self.create_user(
            national_code=national_code,
            is_admin=True,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user

    
class Patients(BaseModel ,AbstractBaseUser ,PermissionsMixin):
    national_code = models.CharField(verbose_name="national_code address",max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()
    
    USERNAME_FIELD = "national_code"
    def __str__(self):
        return self.national_code

    def is_staff(self):
        return self.is_admin
