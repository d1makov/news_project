from . import views
from django.urls import path

urlpatterns = [
    path('', views.posts_list, name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]