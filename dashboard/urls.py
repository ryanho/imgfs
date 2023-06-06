from django.urls import path
from .views import ImageListView, UserListView, DeleteImageView

urlpatterns = [
    path('', ImageListView.as_view(), name='ImageListView'),
    path('<str:pk>/delete/', DeleteImageView.as_view(), name='DeleteImageView'),
    path('user/', UserListView.as_view(), name='UserListView')
]
