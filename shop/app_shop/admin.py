from PIL import Image
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class NotbookAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.fields['image'].help_text = mark_safe(
            '''<span style="color:red; font-size:14px;">Image was cut if size bigger than {}x{}</span>
            '''.format(
                *Product.MAX_RESOLUTION
            )
        )


class NotebookAdmin(admin.ModelAdmin):
    form = NotbookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.fields['image'].help_text = mark_safe(
            '''<span style="color:red; font-size:14px;">Image was cut if size biger than {}x{}</span>
            '''.format(
                *Product.MAX_RESOLUTION
            )
        )
        if not self.fields['sd']:
            self.fields['sd_max_volume'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_max_volume'] = None
        return self.cleaned_data


class SmartphoneAdmin(admin.ModelAdmin):
    change_form_template = 'app_shop/admin.html'
    form = SmartphoneAdminForm

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
admin.site.register(Order)
