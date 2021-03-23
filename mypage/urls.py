from django.urls import path

from mypage.views import FavoriteCreate, ReviewView

urlpatterns = [
    path('/favoritecreate', FavoriteCreate.as_view()),
    path('/review', ReviewView.as_view()),
    # path('/favorateview', FavoriteView.as_view()),
]