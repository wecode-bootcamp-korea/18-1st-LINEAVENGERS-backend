from django.urls import path

from product.views import (
    MainCategoryView, ProductView,
    ProducListView, MainProductView)

urlpatterns = [
    path('', ProducListView.as_view()),
    path('/mainCategory', MainCategoryView.as_view()),
    path('/mainProduct', MainProductView.as_view()),
    path('/modal/<int:product_id>', ProductView.as_view()),
]