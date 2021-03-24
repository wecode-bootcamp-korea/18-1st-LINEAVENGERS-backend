from django.urls import path

from product.views import (
    MainCategoryView, 
    ProductDetailView,
    ProductListView, 
    MainProductView,
    ProductListView,
    ProductReviewView,
    ProductQnaView,
    MyProductQnaView,
    QnaDetailView)

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/main-category', MainCategoryView.as_view()), 
#   path('/sub-category/<int:menu_id>', SubCategoryView.as_view()), 
    path('/main-product', MainProductView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view()),
    path('/<int:product_id>/qna', ProductQnaView.as_view()),
    path('/<int:product_id>/myqna', MyProductQnaView.as_view()),
    path('/<int:product_id>/qna/<int:question_id>', QnaDetailView.as_view()),
]