from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title


class Notebook(Product):

    diagonal = models.CharField(max_length=90, verbose_name='Diagonal')
    display_type = models.CharField(max_length=90, verbose_name='Display type')
    processor_freq = models.CharField(max_length=90, verbose_name='Freq')
    ram = models.CharField(max_length=90, verbose_name='Ram')
    video = models.CharField(max_length=90, verbose_name='Video')
    time_without_charge = models.CharField(max_length=90, verbose_name='Time working without harge')

    def __str__(self):
        return f'{self.category.name} : {self.title}'


class Smartphones(Product):
    
    diagonal = models.CharField(max_length=90, verbose_name='Diagonal')
    display_type = models.CharField(max_length=90, verbose_name='Display type')
    resolution = models.CharField(max_length=90, verbose_name='Resolution')
    accum_volume = models.CharField(max_length=90, verbose_name='Accum')
    ram = models.CharField(max_length=90, verbose_name='Ram')
    sd = models.CharField(max_length=90, verbose_name='SD')
    sd_max_volume = models.CharField(max_length=90, verbose_name='Max volume SD')
    main_cam = models.CharField(max_length=90, verbose_name='Main camera')
    front_cam = models.CharField(max_length=90, verbose_name='Fronta camera')


    def __str__(self):
        return f'{self.category.name} : {self.title}'


class Tv(Product):
    pass


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
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


