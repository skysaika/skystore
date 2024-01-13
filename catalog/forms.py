from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Форма создания продукта"""
    class Meta:
        model = Product
        #только 1 вариант:
        #fields = '__all__'
        fields = ('category', 'name', 'image', 'description', 'price', 'available')
        #exclude = ('slug',)
