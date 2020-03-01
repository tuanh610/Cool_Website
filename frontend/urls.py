from django.urls import path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('new_search/', views.new_search, name='new_search'),
    path('all_mobiles/?page=<int:page>', views.all_mobiles, name='all_mobiles'),
    path('mobiles_byPrices/?dev=<str:dev>&low=<int:low>&high=<int:high>&page=<int:page>',
         views.search_PriceRange, name='mobile_byprice'),
    path('submit_photo/', views.submit_photo, name='submit_photo'),
    path('view_photos/?mode=<int:mode>&page=<int:page>', views.view_photos, name='view_photos'),
    path('view_photos/?mode=<int:mode>&page=<int:page>&username=<str:username>',
         views.view_photos, name='view_photos'),
    path('view_drafts/?mode=<int:mode>&page=<int:page>', views.view_drafts, name='view_drafts'),
    path('photo/<uuid:pk>', views.photo_detail, name='photo_detail'),
    path('drafts/publish', views.publish_draft, name='publish_draft'),
    path('drafts/delete', views.delete_draft, name='delete_draft'),
]
