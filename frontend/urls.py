from django.urls import path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_search/', views.new_search, name='new_search'),
    path('all_mobiles/?page=<int:page>', views.all_mobiles, name='all_mobiles'),
    path('about/', views.about, name='about')
]
