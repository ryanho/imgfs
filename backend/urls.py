from django.urls import path
from .views import HomeView, ShowImageView, get_image
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60 * 60)(HomeView.as_view()), name='HomeView'),
    path('<str:cid>', cache_page(60 * 60)(ShowImageView.as_view()), name='ShowImageView'),
    path('<str:cid>/<str:filename>', cache_page(60 * 60)(get_image), name='GetImage'),
]
