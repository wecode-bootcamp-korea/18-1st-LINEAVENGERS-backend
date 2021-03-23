from django.urls import path

from product.views import (
    MainCategoryView, 
    ProductView,
    ProducListView, 
    MainProductView,
    ListView)

urlpatterns = [
    path('', ProducListView.as_view()),
    path('/main-category', MainCategoryView.as_view()), #path변경 필요.
    path('/main-product', MainProductView.as_view()),   #
    path('/detail/<int:product_id>', ProductView.as_view()),
    path('/list', ListView.as_view()),
#    path('/menu', MainCategoryView.as_view()),
#    path('/menu/<int:menu_id>', ListCategoryView.as_view()),
]