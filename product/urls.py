from django.urls import path

from product.views import (
    ProductListView, CategoryListView, 
    MainCategoryView, ProductDetailView,
    ProductView)

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/category', CategoryListView.as_view()),
    path('/mainCategory', MainCategoryView.as_view()),
    path('/mainProduct', ProductListView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    path('/test1', ProductView.as_view()),
]