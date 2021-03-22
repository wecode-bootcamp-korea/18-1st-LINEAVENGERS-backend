from django.urls import path

from .views import UserSignUp, UserSignIn, Activate, LoginIdExist

urlpatterns = [
   path('/signup', UserSignUp.as_view()),
   path('/signin', UserSignIn.as_view()),
   path('/activate/<str:uidb64>/<str:token>', Activate.as_view()),
   path('/loginexist', LoginIdExist.as_view()),
]