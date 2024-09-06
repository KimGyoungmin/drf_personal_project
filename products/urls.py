from django.urls import path
from . import views

app_name="products"

urlpatterns =[
    path('', views.ProductsListView.as_view(), name="productlist"),
    path('<int:product_id>/', views.ProductsDetailView.as_view(), name="productdetail"),
]