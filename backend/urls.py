from django.urls import path
from .views import HomeView, ShowImageView, get_image
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', HomeView.as_view(), name='HomeView'),
    path('<str:cid>', ShowImageView.as_view(), name='ShowImageView'),
    path('<str:cid>/<str:filename>', get_image, name='GetImage'),
]
