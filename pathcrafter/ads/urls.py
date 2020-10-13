from django.urls import path
from . import views

urlpatterns = [
    path('postad/', views.PostAdPage.as_view(), name='')
    ]