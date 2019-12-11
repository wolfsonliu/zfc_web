from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'zfc'
urlpatterns = [
    path('', views.home, name='home'),
    path('document/', views.document, name='document'),
    path('about/', views.about, name='about'),
    path('<job_id>/download/', views.download, name='download'),
    url(
        'robots.txt',
        TemplateView.as_view(
            template_name="robots.txt", content_type='text/plain'
        )
    ),
    path('job/<job_id>/', views.job, name='job'),
]
