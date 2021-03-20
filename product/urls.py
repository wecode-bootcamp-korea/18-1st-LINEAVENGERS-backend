from django.urls import path

from product.views import ProductListView, CategoryListView, CategoryListView2, MainCategoryView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/category', CategoryListView.as_view()),
    path('/category2', CategoryListView2.as_view()),
    path('/mainCategory', MainCategoryView.as_view()),
    path('/mainProduct', ProductListView.as_view()),
    path('/detail', ProductDetailView.as_view()),
]