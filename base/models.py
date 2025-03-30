from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.timezone import now

# ✅ User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        username = username.lower()
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, first_name, last_name, password, **extra_fields)

# ✅ Fixed User Model (Only One)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)
    
    # ✅ Fix Many-to-Many Relationships for groups and permissions
    groups = models.ManyToManyField(Group, related_name="user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_set", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email

# ✅ Contact Message Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

# ✅ Fixed Donation Model (Removed Duplicates)
class Donation(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    other_donation = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='donation_photos/', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=now, blank=False)

    def __str__(self):
        return f"{self.name} - ${self.amount}"
    

class Recent_Donation(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    other_donation = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='donation_photos/', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=now, blank=False)

    def __str__(self):
        return f"{self.name} - ${self.amount}"

# ✅ Topic Model
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# ✅ Room Model
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="rooms")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name



# ✅ Subscriber Model
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# ✅ Message Model
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:50]
