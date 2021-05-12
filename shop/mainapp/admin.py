from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.utils.safestring import mark_safe
from xdg.Exceptions import ValidationError
from .models import *
from PIL import Image

class NoebookAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '''<span style="color:red; font-size:14px;">
                    Load image (min {}x{}, max{}x{})
               </span>'''.format(*self.MIN_RESOLUTION, *self.MAX_RESOLUTION))

    def clean_image(self):
        image = self.clean_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.width > max_width or img.height > max_height:
            raise ValidationError('Big image!')
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

