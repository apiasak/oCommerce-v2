from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout


from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout',logout,name='logout')
]