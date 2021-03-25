from django.urls import path

from .views import CartList, CartDetailView

urlpatterns = [
   path('', CartList.as_view()),
   path('/<int:product_id>', CartDetailView.as_view()),
]