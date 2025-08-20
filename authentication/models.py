from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


#----------- Custom user manager--------------

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
#----------- Custom user Model ----------------


class CustomUser(AbstractUser):
   
    USER_TYPES = (
        ('user', 'User'),
        ('employee', 'Employee'),
    )
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number'] 

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.user_type} - {self.email}"

#---------------- EMPLOYEE PROFILE ----------------

class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee_profile")
    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    skills = models.ManyToManyField("Skill", blank=True)

    def __str__(self):
        return f"Employee: {self.full_name or self.user.email}"


#---------------- USER PROFILE ----------------

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_pics/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"User: {self.full_name or self.user.email}"


# ---------------- SKILLS ----------------

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
