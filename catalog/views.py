import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView

from catalog.models import Product, Category


class IndexView(TemplateView):
    """Класс контроллера главной страницы"""
    template_name = 'catalog/index.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        """Метод GET для главной страницы"""
        context = {}
        available_products = Product.objects.filter(available=True)
        random_products = random.sample(list(available_products), min(3, len(available_products)))
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
    fields = '__all__'
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
    fields = '__all__'
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
    fields = 'category', 'name', 'slug', 'image', 'description', 'price', 'available'
    success_url = reverse_lazy('catalog:product_list')  # путь до страницы после создания

    def form_valid(self, form):
        """Генерация динамического slug на основе названия продукта"""
        form.instance.slug = slugify(form.instance.name)
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('name', 'Товар с таким названием уже существует.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание продукта'
        return context


class ProductUpdateView(UpdateView):
    """Класс контроллера страницы редактирования продукта"""
    model = Product
    template_name = 'catalog/product_form.html'
    fields = '__all__'
    # success_url = reverse_lazy('catalog:product_list')  # путь до страницы после сохранения

    def get_success_url(self):
        """Перенаправляю на страницу продукта"""
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        """Метод для генерации slug на основе названия продукта"""
        form.instance.slug = slugify(form.instance.name)
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('name', 'Товар с таким названием уже существует.')
            return self.form_invalid(form)


class ProductListView(ListView):
    """Класс контроллера страницы со всеми товарами"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'object_list'
    paginate_by = 3  # 3 товара на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все товары'
        return context


class ProductDetailView(DetailView):
    """Класс контроллера страницы карточки продукта"""
    model = Product
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
