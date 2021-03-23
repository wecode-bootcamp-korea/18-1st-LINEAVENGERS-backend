from django.urls import path

from product.views import (
    MainCategoryView, 
    ProductView,
    ProductListView, 
    MainProductView,
    ListView)

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/main-category', MainCategoryView.as_view()), 
    path('/main-product', MainProductView.as_view()),
    path('/detail/<int:product_id>', ProductView.as_view()),
    path('/list', ListView.as_view()),
    path('/list-category', ListView.as_view()),
#    path('/menu', MainCategoryView.as_view()),
#    path('/menu/<int:menu_id>', ListCategoryView.as_view()),
]