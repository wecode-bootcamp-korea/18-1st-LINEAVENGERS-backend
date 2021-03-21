from django.urls import path

from product.views import (
    ProductListView, CategoryListView, 
    MainCategoryView, ProductDetailView,
    ProductView, MainView)

urlpatterns = [
    #제품리스트 상품 조회.
    path('', ProductListView.as_view()),
    #제품리스트 카테고리 조회.
    path('/category', CategoryListView.as_view()),
    #메인 카테고리 조회
    path('/mainCategory', MainCategoryView.as_view()),
    #메인 상품 조회
    path('/mainProduct', ProductListView.as_view()),
    #제품상세
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    #제품 리스트 조회 합본
    path('/test1', ProductView.as_view()),
    #메인화면 조회 합본
    path('/test2', MainView.as_view())
]