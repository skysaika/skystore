from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contact, IndexView, CategoryListView, ProductListView, \
    CategoryCreateView, ProductByCategoryView, ProductCreateView, ProductDetailView, ProductUpdateView, \
    ProductDeleteView, CategoryUpdateView, CategoryDetailView, CategoryDeleteView

# название приложения
app_name = CatalogConfig.name



urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # путь до главной страницы
    path('contact/', contact, name='contact'),  # путь до страницы контактов FBV

    path('create_category/', CategoryCreateView.as_view(), name='create_category'),  # создание категории
    path('edit_category/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),  # редактирование категории
    path('category_list/', CategoryListView.as_view(), name='category_list'),  # путь до страницы категорий
    path('category_detail/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  # карточка категории
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),  # удаление категории


    path('<int:pk>/product_list/', ProductByCategoryView.as_view(), name='category_product_list'),  # продукты по категориям
    path('product_list/', ProductListView.as_view(), name='product_list'),  # путь до страницы со всеми товарами
    path('create_product/', ProductCreateView.as_view(), name='create_product'),  # создание продукта
    path('product_detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),  # карточка продукта
    path('product_edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),  # редактирование продукта
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),  # удаление продукта


    # path('toggle_availability/<int:pk>/', toggle_availability, name='toggle_availability'),  # переключение статуса
]
