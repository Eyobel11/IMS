import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.urls import reverse, reverse_lazy

user_type = [
    ('Manager', "manager"),
    ('Registeror', "registeror"),
    ('Engineer', "Engineer"),
    ('Staff', "staff"),
    ('Admin', "Admin"),
    ('Other', "Other"),
]

status =[
    ('pending', "pending"),
    ('shipped', "shipped"),
]

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    user_name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    user_type = models.CharField(choices=user_type, default="Engineer", max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_pic/", null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='warehouse_user_groups',  # Adding related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='warehouse_user_permissions',  # Adding related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

    def __str__(self):
        return f"{self.first_name.upper()} {self.last_name.upper()}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Stock(models.Model):
    current_level = models.PositiveIntegerField(default=0)
    stock_no = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='stocks')

    def __str__(self):
        return f"Stock {self.id} in {self.category.name} - Current Level: {self.current_level}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        return self.name


class Order(models.Model):
    quantity = models.IntegerField()
    order_date = models.DateField()
    status = models.CharField(choices=status,default='shipped', max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')


    def __str__(self):
        return f"Order {self.id} - {self.item.name}"

class MaterialRequest(models.Model):
    request_date = models.DateField()
    status = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='material_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_requests')

    def __str__(self):
        return f"Request {self.id} by {self.user.user_name}"


# models.py

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.user_name} - {self.created_at}"

