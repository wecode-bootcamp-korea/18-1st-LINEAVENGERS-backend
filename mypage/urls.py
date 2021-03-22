from django.urls import path

from mypage.views import FavoriteCreate, ReviewCreate, ReviewClick

urlpatterns = [
    path('/favoritecreate', FavoriteCreate.as_view()),
    path('/reviewcreate', ReviewCreate.as_view()),
    path('/reviewclick', ReviewClick.as_view()),
    # path('/favorateview', FavoriteView.as_view()),
]