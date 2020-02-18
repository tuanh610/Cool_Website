from django.urls import path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('new_search/', views.new_search, name='new_search'),
    path('all_mobiles/?page=<int:page>', views.all_mobiles, name='all_mobiles'),
    path('mobiles_byPrices/?dev=<str:dev>&low=<int:low>&high=<int:high>&page=<int:page>',
         views.search_PriceRange, name='mobile_byprice'),
    path('search_result/', views.search_result, name='search_result'),
]
