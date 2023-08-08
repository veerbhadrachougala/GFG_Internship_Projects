from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator



# Product model
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('man', 'Man'),
        ('women', 'Woman'),
        ('kids', 'Kids'),
        ('electronics', 'Electronics'),
        ('mobiles', 'Mobiles'),

    )
    name = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='man')
    description = models.TextField(default='')

    def __str__(self):
        return self.name


# Custumer model
class Customer(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(default='')
    phone = models.IntegerField(default='0000000000')
    password = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.phone


# cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"



# OrderPlaced model
class Orderedplaced(models.Model):
    STATUS_CHOICES = (
    ('accepted','Accepted'),
    ('packed','Packed'),
    ('delivered','Delivered'),
    ('on the way','On the way'),
    ('canceled','Canceled')
    )

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customerName = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    phone = models.BigIntegerField(default='0000000000')
    state = models.CharField(max_length=30,null=True)
    district = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    pin = models.IntegerField(null=True)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.IntegerField(null=True)
    Ordered_date = models.DateTimeField(auto_now_add=True)
    paymentMethod = models.CharField(max_length=255,default='Cash on Delivery')
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Accepted')

    def __str__(self):
        return f"{self.customerName}--- quantity({self.quantity})----  TotalAmount({self.amount}) ---  status({self.status})"


# Coupon model
class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount_price = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    # valid_from = models.DateTimeField()
    # valid_to = models.DateTimeField()

    def __str__(self):
        return self.code