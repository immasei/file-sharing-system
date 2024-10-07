from django.db.models import *
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):    
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    username = CharField(max_length=30)
    email = EmailField(unique=True)
    quota_limit = DecimalField(decimal_places=1, default=300.0, max_digits=4)
    quota_used = DecimalField(decimal_places=1, default=0.0, max_digits=4)
    avatar = URLField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f'{self.name} ({self.email})' 
