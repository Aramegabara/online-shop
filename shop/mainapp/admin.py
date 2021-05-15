from PIL import Image
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_max_volume'].widget.attrs.update({
                'readonly':True, 'style': 'background: lightgray'
            })

class NotbookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '''<span style="color:red; font-size:14px;">
                    Load image (min {}x{}, max{}x{})
               </span>'''.format(*Product.MIN_RESOLUTION, *Product.MAX_RESOLUTION))

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError(f'Size image biger than 100 kb! Img = {round(image.size * 0.00097656)} kb')
        if img.width < min_width or img.height < min_height:
            raise ValidationError(f'Small image! {img.width}x{img.height}')
        if img.width > max_width or img.height > max_height:
            raise ValidationError(f'Big image! {img.width}x{img.height}')
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotbookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'mainapp/admin.html'


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

