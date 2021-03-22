from django.urls import path

from order.views import CartView, OrderView, CartOrderView

urlpatterns = [
    path('/<int:product_id>', OrderView.as_view()),
    path('/cart', CartOrderView.as_view()),
    path('/cart/<int:product_id>', CartView.as_view()),
]