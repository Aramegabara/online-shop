from django.contrib import admin
from xdg.Exceptions import ValidationError
from .models import *
from django.forms import ModelChoiceField, ModelForm
from PIL import Image

class NoebookAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)
    # MAX_RESOLUTION = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Download image (min {}x{})'.format(*self.MIN_RESOLUTION)

    def clean_image(self):
        image = self.clean_data['image']
        img = Image.open(image)
        # print(img.width, img.height)
        min_height, min_width = self.MIN_RESOLUTION
        if img.width < min_width or img.height < min_height:
            raise ValidationError('Small image!')
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NoebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

