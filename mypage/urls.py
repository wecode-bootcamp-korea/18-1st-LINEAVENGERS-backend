from django.urls import path

from mypage.views import FavoriteView, ReviewView

urlpatterns = [
    path('/favorite', FavoriteView.as_view()),
    path('/review', ReviewView.as_view()), 
]