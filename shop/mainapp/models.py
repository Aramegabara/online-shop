from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


User = get_user_model()

# Models
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Customer
#6 Specification
#7 Order

class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name='Category')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_product')
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sum_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Sum')

    def __str__(self):
        return f'Product : {self.product.title} (in Cash)'


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Owner', on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True,  related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    sum_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Sum')

    def __str__(self):

        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone')
    address = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return f"Customer : {self.user.first_name} {self.user.last_name}"


class Specification(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=90, verbose_name='Name for specification')

    def __str__(self):
        return f"Specification for product {self.name}"
