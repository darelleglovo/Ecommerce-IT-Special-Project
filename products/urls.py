# Django 2.0
from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='home'),
    path('products/<slug:slug>/', views.ProductDetailSlugView.as_view(), name='detail'),
    path('products/category/<slug:category_slug>/', views.list_products_by_category, name='list_products_by_category'),
    path('products/subcategory/<slug:subcategory_slug>/', views.list_products_by_subcategory, name='list_products_by_subcategory'),
    path('reports/', views.reports_page, name='reports_page'), #changes
    path('report_result/', views.reports_result, name='reports_result'), #changes
    # path('featured/', views.ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', views.ProductFeaturedDetailView.as_view()),
    # path('products-fbv/', views.product_list_view),
    # path('products/<int:pk>/', views.ProductDetailView.as_view()),
    # path('products-fbv/<int:pk>/', views.product_detail_view),
]