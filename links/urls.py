from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.link_list, name='link_list'),
    path('register/', views.register,name='register'),
     path('login/',auth_views.LoginView.as_view(
            template_name='links/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),

    path('logout/',auth_views.LogoutView.as_view(),
        name='logout',
    ),
    path('add/', views.link_create, name='link_create'),
    path('edit/<int:pk>/', views.link_update, name='link_update'),
    path(
        'toggle/<int:pk>/',
        views.link_toggle_visited,
        name='link_toggle_visited',
    ),
    path('delete/<int:pk>/', views.link_delete, name='link_delete'),
]
