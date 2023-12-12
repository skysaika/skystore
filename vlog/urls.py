from django.urls import path

from vlog.apps import VlogConfig
app_name = VlogConfig.name


urlpatterns = [
    path('create_post/', ..., name='create_post'),  # создание поста
    path('edit_post/<int:pk>/', ..., name='update_post'),  # редактирование поста
    path('post_detail/<int:pk>/', ..., name='post_detail'),  # карточка поста
    path('post_list/', ..., name='post_list'),  # путь до страницы со всеми постами
    path('delete_post/<int:pk>/', ..., name='delete_post'),  # удаление поста
]
