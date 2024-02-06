import random

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db import IntegrityError, transaction
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Category, Version


class IndexView(TemplateView):
    """Класс контроллера главной страницы"""
    template_name = 'catalog/index.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        """Метод GET для главной страницы"""
        context = {}
        available_products = Product.objects.filter(available=True)
        # random_products = random.sample(list(available_products), min(3, len(available_products)))
        random_products = Product.objects.filter(available=True).order_by('?')[:3]
        context['title'] = 'Главная страница'

        # Пагинация продуктов
        paginator = Paginator(random_products, self.paginate_by)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['object_list'] = products
        context['paginator'] = paginator
        context['is_paginated'] = True  # добавляем информацию о пагинации в контекст

        return render(request, self.template_name, context)


def contact(request):
    """Контроллер страницы контактов на FBV"""
    # метод POST - получение данных, не забудь вернуть context
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'name:{name}, email:{email}, {message}')
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contact.html', context)


class CategoryCreateView(CreateView):
    """Класс контроллера страницы создания категорий"""
    model = Category
    template_name = 'catalog/category_form.html'
    fields = 'name', 'description'
    # success_url = reverse_lazy('catalog:category_list')

    def get_success_url(self):
        return reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        """Метод для генерации slug на основе названия категории"""
        form.instance.slug = slugify(form.instance.name)
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('name', 'Категория с таким названием уже существует.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание категории'
        return context


class CategoryUpdateView(UpdateView):
    """Класс контроллера страницы редактирования категорий"""
    model = Category
    template_name = 'catalog/category_form.html'
    fields = 'name', 'description'
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        """Генерация slug на основе названия категории"""
        form.instance.slug = slugify(form.instance.name)
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('name', 'Категория с таким названием уже существует.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование категории'
        return context


class CategoryListView(ListView):
    """Класс контроллера страницы категорий"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'object_list'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список категорий'
        if settings.CACHE_ENABLED:
            key = 'category_list'
            category_list = cache.get(key)
            if category_list is None:
                category_list = list(Category.objects.all())
                cache.set(key, category_list, 60)  # Кэширование на 60 секунд
                return category_list
            else:
                return Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    """Класс контроллера страницы карточки категории"""
    model = Category
    template_name = 'catalog/category_detail.html'
    extra_context = {'title': 'Карточка категории'}


class CategoryDeleteView(DeleteView):
    """Класс контроллера страницы удаления категорий"""
    model = Category
    template_name = 'catalog/category_confirm_delete.html'
    success_url = reverse_lazy('catalog:category_list')


class ProductByCategoryView(ListView):
    """Класс контроллера страницы отфильтрованных товаров по категориям"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'object_list'
    paginate_by = 4  # 4 товаров на странице

    def get_queryset(self):
        # Получаем категорию
        category_item = Category.objects.get(pk=self.kwargs['pk'])
        # Фильтруем товары по категории
        queryset = Product.objects.filter(category_id=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем название категории в контекст
        category_item = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Товары категории: {category_item.name}'

        # Добавляем пагинацию к контексту
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['object_list'] = products  # используем переменную для пагинированного списка
        context['is_paginated'] = True  # добавляем информацию о пагинации в контекст
        return context


class ProductCreateView(CreateView):
    """Класс контроллера страницы создания продукта"""
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')  # путь до страницы после создания

    def form_valid(self, form):
        """Создаваемый продукт принадлежит текущему пользователю"""
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание продукта'

        return context_data

# ProductUpdateView -> не забыть вставить instance=self.object

class ProductUpdateView(UpdateView):
    """Класс контроллера страницы редактирования продукта"""
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    # success_url = reverse_lazy('catalog:product_detail')  # путь до страницы после сохранения


    def get_success_url(self):
        """Перенаправляю на страницу продукта"""
        return reverse_lazy('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """Получаем продукт и проверяем его владельца"""
        self.object = super().get_object()
        # проверим, что модератор может редактировать этот продукт
        if self.request.user.has_perm('catalog.change_product'):
            return self.object
        if self.object.owner != self.request.user:
            raise Http404('Вы не являетесь владельцем этого продукта')
        return self.object



    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование продукта'

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """ВАлидация формсета и сохранение продукта"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            # Если формсет валиден, сохраняем продукт
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)




class ProductListView(ListView):
    """Класс контроллера страницы со всеми товарами"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'object_list'
    paginate_by = 3  # 3 товара на странице

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Все товары'
        return context_data


class ProductDetailView(DetailView):
    """Класс контроллера страницы карточки продукта"""
    model = Product
    fields = '__all__'
    template_name = 'catalog/product_detail.html'
    paginate_by = 1  # 1 товар на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение всех доступных товаров
        available_products = Product.objects.filter(available=True)

        # Пагинация продуктов
        paginator = Paginator(available_products, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # Проверка владельца
        self.object = super().get_object()
        if self.object.owner == self.request.user or self.request.user.has_perm('catalog.change_product'):
            context['is_owner'] = True

        context['products'] = products
        context['paginator'] = paginator
        context['is_paginated'] = True  # добавляем информацию о пагинации в контекст
        context['title'] = f'Карточка продукта: {context["object"].name}'  # Добавляем заголовок карточки продукта

        return context


class ProductDeleteView(DeleteView):
    """Класс контроллера страницы удаления продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

#пока оставлю, потом может пригодится
# def toggle_availability(request, pk):
#     """Переключатель доступности продукта"""
#     product_item = get_object_or_404(Product, pk=pk)
#     if product_item.available:
#         product_item.available = False
#     else:
#         product_item.available = True
#     product_item.save()
#     return redirect(reverse('catalog:product_list'))
