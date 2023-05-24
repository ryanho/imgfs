from django.urls import path
from .views import HomeView, ShowImageView, get_image

urlpatterns = [
    path('', HomeView.as_view(), name='HomeView'),
    path('<str:cid>', ShowImageView.as_view(), name='ShowImageView'),
    path('<str:cid>/<str:filename>', get_image, name='GetImage'),
]
