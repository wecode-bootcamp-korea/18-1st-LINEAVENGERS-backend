from django.urls import path

from .views import CartList

urlpatterns = [
   path('', CartList.as_view()),
]