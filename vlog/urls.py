from django.urls import path

from vlog.apps import VlogConfig
from vlog.views import VlogPostCreateView, VlogPostListView, VlogPostDetailView, VlogPostUpdateView, VlogPostDeleteView

app_name = VlogConfig.name


urlpatterns = [
    path('create_post/', VlogPostCreateView.as_view(), name='create_post'),  # создание поста
    path('post_list/', VlogPostListView.as_view(), name='post_list'),  # путь до страницы со всеми постами
    path('edit_post/<int:pk>/', VlogPostUpdateView.as_view(), name='edit_post'),  # редактирование поста
    path('post_detail/<int:pk>/', VlogPostDetailView.as_view(), name='post_detail'),  # карточка поста
    path('delete_post/<int:pk>/', VlogPostDeleteView.as_view(), name='delete_post'),  # удаление поста
]
