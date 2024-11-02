from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='web-home'),
    path('about/', views.about, name='web-about'),
    path('projects/', views.github_repos, name='web-projects'),
    path('contact/', views.contact_view, name='web-contact'),  # Use contact_view for the form
    path('success/', views.success_view, name='success'),  # Ensure success view exists
]
