from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_category():
        return Category.objects.all()

class Product(models.Model):
    brand = models.CharField(max_length=100,default="Roadster")
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    price = models.FloatField()
    image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @staticmethod
    def get_all_products_by_categoryslug(category_slug):
        if category_slug:
            return Product.objects.filter(category = category_slug)
        else:
            return Product.get_all_products();

class CartItem(models.Model):
    cart_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
