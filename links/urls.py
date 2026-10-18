from django.urls import path
from . import views


urlpatterns = [
    path('', views.link_list, name='link_list'),
    path('add/', views.link_create, name='link_create'),
    path('edit/<int:pk>/', views.link_update, name='link_update'),
    path(
        'toggle/<int:pk>/',
        views.link_toggle_visited,
        name='link_toggle_visited',
    ),
    path('delete/<int:pk>/', views.link_delete, name='link_delete'),
]
