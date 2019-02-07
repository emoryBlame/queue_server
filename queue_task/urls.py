from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('send/', views.send),
    path('result/', views.result),
    path('start_tasks/', views.start_tasks),
]
