from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from vlog.models import VlogPost


# Create your views here.
class VlogPostCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_form.html'
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('vlog:post_list')


    # def get_object(self, queryset=None):
    #     """Проверяем что пользователь не может редактировать чужой пост"""
    #     self.object = super().get_object(queryset)
    #     if self.object.owner != self.request.user and not self.request.user.is_staff:
    #         raise Http404('Вы не можете редактировать чужую собаку')  # может владелец и модератор
    #     return self.object


class VlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_form.html'
    fields = ('title', 'content', 'preview', 'is_published')
    # success_url = reverse_lazy('vlog:post_list')




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


class VlogPostDetailView(LoginRequiredMixin, DetailView):
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

    def get_queryset(self):
        """Если не owner или staff, то не может просматривать чужой пост"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset



class VlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления поста"""
    model = VlogPost
    template_name = 'vlog/vlogpost_confirm_delete.html'
    success_url = reverse_lazy('vlog:post_list')

