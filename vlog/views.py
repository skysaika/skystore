
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from vlog.models import VlogPost


# Create your views here.
class VlogPostCreateView(CreateView):
    """Контроллер создания поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_form.html'
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('vlog:post_list')


    # def form_valid(self, form):
    #     """метод для генерации slug на основе заголовка поста"""
    #     if form.is_valid():
    #         new_post = form.save()
    #         new_post.slug = slugify(new_post.title)
    #         new_post.save()
    #
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context


class VlogPostUpdateView(UpdateView):
    """Контроллер редактирования поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_form.html'
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('vlog:post_list')

    def get_success_url(self):
        """Перенаправление после редактирования на страницу поста"""
        return reverse('vlog:post_detail', args=[self.kwargs.get('pk')])

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

    def get_queryset(self):
        """Выводим только опубликованные посты"""
        return VlogPost.objects.filter(is_published=True)


class VlogPostDetailView(DetailView):
    """Контроллер просмотра поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_detail.html'
    extra_context = {'title': 'Просмотр поста'}

    def get_object(self, queryset=None):
        """Метод для счетчика просмотров"""
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class VlogPostDeleteView(DeleteView):
    """Контроллер удаления поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_confirm_delete.html'
    success_url = reverse_lazy('vlog:post_list')

