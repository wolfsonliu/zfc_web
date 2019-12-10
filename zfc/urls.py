from django.urls import path

from . import views

app_name = 'zfc'
urlpatterns = [
    path('', views.home, name='home'),
    path('document/', views.document, name='document'),
    path('about/', views.about, name='about'),
    path('<job_id>/download/', views.download, name='download'),
    path('<job_id>/', views.job, name='job'),
]
