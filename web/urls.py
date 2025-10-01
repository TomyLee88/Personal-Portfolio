from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='web-home'),
    path('about/', views.about, name='web-about'),
    path('caseStudies/', views.caseStudies, name='web-caseStudies'),
    path('projects/', views.github_repos, name='web-projects'),
    path('contact/', views.contact_view, name='web-contact'),  
    path('success/', views.success_view, name='success'),  
]
