from django.urls import path
from . import views

urlpatterns = [
    path('', views.drive, name='drive'),
    path('create-upload/', views.create_upload, name='create_upload'),
    path('complete-upload/', views.complete_upload, name='complete_upload'),
]