from django.contrib import admin

from catalog.models import Category, Product, Version


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка модели Категория"""
    list_display = ('pk', 'name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка модели Продукт"""
    list_display = ['name', 'pk', 'slug', 'price', 'category',
                    'available', 'created', 'updated']
    list_filter = ['category', 'available', 'created', 'updated']
    search_fields = ['name', 'slug', 'description']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'active_version')
    list_filter = ('product', 'version_number', 'version_name', 'active_version')
