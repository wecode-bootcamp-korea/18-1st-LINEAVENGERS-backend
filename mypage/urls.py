from django.urls import path

from .views import Favorite 

urlpatterns = [
    path('/favorite', Favorite.as_view())
]