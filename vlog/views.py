from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from vlog.models import VlogPost


# Create your views here.
class VlogPostCreateView(CreateView):
    """Контроллер создания поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_form.html'
    fields = '__all__'
    success_url = reverse_lazy('vlog:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context


class VlogPostUpdateView(UpdateView):
    """Контроллер редактирования поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_form.html'
    fields = '__all__'
    success_url = reverse_lazy('vlog:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование поста'
        return context


class VlogPostListView(ListView):
    """Контроллер списка постов"""
    model = VlogPost
    template_name = 'vlog/vlogpost_list.html'
    extra_context = {'title': 'Список постов'}
    paginate_by = 4


class VlogPostDetailView(DetailView):
    """Контроллер просмотра поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_detail.html'
    extra_context = {'title': 'Просмотр поста'}


class VlogPostDeleteView(DeleteView):
    """Контроллер удаления поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_confirm_delete.html'
    success_url = reverse_lazy('vlog:post_list')

