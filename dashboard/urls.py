from django.urls import path
from .views import ImageListView, UserListView

urlpatterns = [
    path('', ImageListView.as_view(), name='ImageListView'),
    path('user/', UserListView.as_view(), name='UserListView')
]
