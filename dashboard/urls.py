from django.urls import path
from .views import ImageListView

urlpatterns = [
    path('', ImageListView.as_view(), name='ImageListView'),
]
