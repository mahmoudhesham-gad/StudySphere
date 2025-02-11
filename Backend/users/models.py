from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    The create_user method is used to create a regular user with basic authentication functionality.
    """
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        

        return user

    """
    The create_superuser method is used to create a superuser with basic authentication functionality.
    """
    def create_superuser(self, email, username, password, **extra_fields):
        # Ensure the superuser flags are set to True by default
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Create the user using the superuser's fields
        return self.create_user(email, username, password, **extra_fields)

  
class User(AbstractUser):
  """
  The User model is used to store user information.
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=100, unique=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  """Replaces default user manager with a custom implementation"""
  objects = CustomUserManager()


  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def has_perm(self, perm, obj=None):
      """Check if user has a specific permission"""
      return self.is_superuser

  def has_module_perms(self, app_label):
      """Check if user has permissions for a specific app"""
      return self.is_superuser

  def __str__(self):
    return self.email
  

class Profile(models.Model):
  """
  The Profile model is used to store user profile information.
  """
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  bio = models.TextField(null=True, blank=True)
  Affiliation = models.CharField(max_length=255, null=True, blank=True)
  # profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.user.email
  
