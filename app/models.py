from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
import random


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    code = models.CharField(max_length=4)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)
    
    def save(self, *args, **kwargs):
        number = random.randint(1000,9999)
        self.code = number
        super().save(*args, **kwargs)


MAIN_CATEGORY_CHOICES = (
    ('Clothes and Accessories', 'Clothes and Accessories'),
    ('Electronics', 'Electronics'),
    ('Home and living', 'Home and Living'),
    ('Books and stationery', 'Books and Stationery'),
    ('Sports and outdoors', 'Sports and Outdoors'),
    ('Beauty and cosmetics', 'Beauty and Cosmetics'),
    ('Toys and Games', 'Toys and games'),
    ('Pets and Pet Supplies', 'Pets and pet Supplies'),
    ('Home improvement', 'Home improvement')
)

SUB_CATEGROY_CHOICES = (
    ("Men's Clothing", "Men's Clothing"),
    ("Women's Clothing", "Women's Clothing"),
    ("Kitchen", "Kitchen"),
    ("Accessories", "Accessories"),
    ("Smartphones", "Smartphones"),
    ("Laptops", "Laptops"),
    ("Audio Device", "Audio Device"),
    ("Furniture", "Furniture"),
    ("Kitchen", "Kitchen"),
    ("Decor", "Decor"),
    ("Fiction", "Fiction"),
    ("Novels", "Novels"),
    ("Magazines", "Magazines"),
    ("Outdoor Gear", "Outdoor Gear"),
    ("Sport's Equipment", "Sport's Equipment"),
    ("Active Wear", "Active Wear"),
    ("Makeup", "Makeup"),
    ("Skincare", "Skincare"),
    ("Haircare", "Haircare"),
    ("Fragrance", "Fragrance"),
    ("Children's Toys", "Children's Toys"),
    ("Board Games", "Board Games"),
    ("Outdoor Games", "Outdoor Games"),
    ("Video Games", "Video Games"),
    ("Educational Toys", "Educational Toys"),
    ("Puzzles", "Puzzles"),
    ("Pet Food", "Pet Food"),
    ("Toys and Accessories", "Toys and Accessories"),
    ("Grooming and Health", "Grooming and Health"),
    ("Pet Carries", "Pet Carries"),
    ("Small Animal Supplies", "Small Animal Supplies"),
    ("Power Tools", "Power Tools"),
    ("Hand Tools", "Hand Tools"),
    ("Painting Supplies", "Painting Supplies"),
    ("Home Security", "Home Security"),
    ("Lightning and Electrical", "Lightning and Electrical"),
    ("Plumbing", "Plumbing"),
    ("Hardware", "Hardware"),
    ("Home Organization", "Home Organization")
)

SUB_TYPE_CHOICES = (
    ("T-Shirts", "T-Shirts"),
    ("Shirts", "Shirts"),
    ("Jeans", "Jeans"),
    ("Jackets", "Jackets"),
    ("Dresses", "Dresses"),
    ("Tops", "Tops"),
    ("Sweaters", "Sweaters"),
    ("Buttons", "Buttons"),
    ("Pants", "Pants"),
    ("Leggins", "Leggins"),
    ("Outwear", "Outwear"),
    ("Hats", "Hats"),
    ("Bags", "Bags"),
    ("Scarves", "Scarves"),
    ("Sunglasses", "Sunglasses"),
    ("Jewelry", "Jewelry"),
    ("Android", "Android"),
    ("iOS", "iOS"),
    ("Windows", "Windows"),
    ("Mac", "Mac"),
    ("Headphones", "Headphones"),
    ("Speakers", "Speakers"),
    ("Earphones", "Earphones"),
    ("Living Room", "Living Room"),
    ("Bedroom", "Bedroom"),
    ("Dining Room", "Dining Room"),
    ("Cookware", "Cookware"),
    ("Cutlery", "Cutlery"),
    ("Appliances", "Appliances"),
    ("Wall Art", "Wall Art"),
    ("Rugs", "Rugs"),
    ("Nails and Screws", "Nails and Screws"),
    ("Drills", "Drills"),
    ("Dog Food", "Dog Food"),
    ("Action Figures", "Action Figures"),
    ("Face", "Face"),
    ("Camping", "Camping"),
    ("Mystery", "Mystery"),
)

SIZES = (
    ("Xtra Large", "Xtra Large"),
    ("Large", "Large"),
    ("Medium", "Medium"),
    ("Small", "Small")
)


class Product(models.Model):
    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES, null=True)
    sub_category = models.CharField(max_length=50, choices=SUB_CATEGROY_CHOICES, null=True)
    sub_type_category = models.CharField(max_length=50, choices=SUB_TYPE_CHOICES, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=50, choices=SIZES)
    color = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    def __str__(self):
        return str(self.product)

