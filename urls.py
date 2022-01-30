from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.registration), #forgot
    path('login', views.login), #forgot
    path('success', views.success),
    path('logout', views.index),
]
