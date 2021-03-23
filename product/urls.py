from django.urls import path

from product.views import (
    MainCategoryView, 
    ProductDetailView,
    ProductListView, 
    MainProductView,
    ProductListView)

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/main-category', MainCategoryView.as_view()), 
    path('/main-product', MainProductView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
#    path('/review/<int:product_id>', ProductDetailView.as_view()),
#    path('/qna/<int:product_id>', ProductDetailView.as_view()),
]