from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxInput

from catalog.models import Product, Version


class StyleFormMixin:
    """Миксин для стилизации форм"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'



class ProductForm(StyleFormMixin, forms.ModelForm):
    """Форма создания продукта"""
    forbidden_words = ['казино', 'криптовалюта', 'крипта',
                       'биржа', 'дешево', 'бесплатно',
                       'обман', 'полиция', 'радар'
                       ]
    class Meta:
        model = Product
        #только 1 вариант:
        #fields = '__all__'
        fields = ('category', 'name', 'image', 'description', 'price', 'available')
        #exclude = ('slug',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name.lower() in self.forbidden_words:
            raise ValidationError('Такое название запрещено для продукта')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if description.lower() in self.forbidden_words:
            raise ValidationError('Такое описание запрещено для продукта')
        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    """Форма создания версии продукта"""
    class Meta:
        model = Version
        fields = '__all__'

    def clean_active_version(self):
        """Метод для проверки активной версии"""
        active_version = self.cleaned_data.get('active_version')
        if len(Version.objects.filter(active_version=True)) > 1 and not active_version:
            raise ValidationError('Должна быть только одна активная версия')
        return active_version



