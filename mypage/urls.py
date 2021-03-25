from django.urls import path

from mypage.views import FavoriteView

urlpatterns = [
    path('/favorite', FavoriteView.as_view())
]