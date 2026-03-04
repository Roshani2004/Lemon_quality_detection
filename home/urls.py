from django.urls import path
from . import views   # VERY IMPORTANT (use dot)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('prediction/', views.prediction, name='prediction'),
]