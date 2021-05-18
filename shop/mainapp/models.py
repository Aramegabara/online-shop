from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(object, viewname ):
    ct_model = object.__class__._meta.model_name
    reverse(viewname, kwargs={'ct_model': ct_model, 'slug': object.slug})


User = get_user_model()


class MinResolutionErrorExeption(Exception):
    pass


class MaxResolutionErrorExeption(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                        reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Notebooks': 'notebook__count',
        'Smartphones': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name='Category')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 1300)
    MAX_IMAGE_SIZE = 102400

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

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.width < min_width or img.height < min_height:
            raise MinResolutionErrorExeption('Small image!')
        if img.width > max_width or img.height > max_height:
            raise MaxResolutionErrorExeption('Big image!')
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__._meta.model_name


class Notebook(Product):

    diagonal = models.CharField(max_length=90, verbose_name='Diagonal')
    display_type = models.CharField(max_length=90, verbose_name='Display type')
    processor_freq = models.CharField(max_length=90, verbose_name='Freq')
    ram = models.CharField(max_length=90, verbose_name='Ram')
    video = models.CharField(max_length=90, verbose_name='Video')
    time_without_charge = models.CharField(max_length=90, verbose_name='Time working without charge')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    
    diagonal = models.CharField(max_length=90, verbose_name='Diagonal')
    display_type = models.CharField(max_length=90, verbose_name='Display type')
    resolution = models.CharField(max_length=90, verbose_name='Resolution')
    accum_volume = models.CharField(max_length=90, verbose_name='Accum')
    ram = models.CharField(max_length=90, verbose_name='Ram')
    sd = models.BooleanField(default=True, verbose_name='slot for SD')
    sd_max_volume = models.CharField(
        max_length=90, null=True, blank=True, verbose_name='Max volume SD'
    )
    main_cam = models.CharField(max_length=90, verbose_name='Main camera')
    front_cam = models.CharField(max_length=90, verbose_name='Fronta camera')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    sum_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Sum')

    def __str__(self):
        return f'Product : {self.content_object.title} (in Basket)'

    def save(self, *args, **kwargs):
        self.sum_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Owner', on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True,  related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    sum_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Sum')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):

        return str(self.id)

    def save(self, *args, **kwargs):
        cart_data = self.product.aggregate(models.Sum('sum_price'), models.Count('id'))
        if cart_data.get('sum_price__sum'):
            self.sum_price = cart_data.get('sum_price__sum')
        else:
            self.sum_price = 0
        self.total_products = cart_data['id__count']
        super().save(*args, **kwargs)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)

    def __str__(self):
        return f"Customer : {self.user.first_name} {self.user.last_name}"

