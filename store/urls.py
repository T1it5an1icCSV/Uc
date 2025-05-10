from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

app_name = 'store'

# API маршруты
router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'products', api_views.ProductViewSet)

api_urlpatterns = [
    path('', api_views.api_root, name='api-root'),
    path('', include(router.urls)),
    path('orders/', api_views.OrdersAPIView.as_view(), name='api-orders'),
]

# Обычные веб-маршруты
urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/complete/<int:order_id>/', views.order_complete, name='order_complete'),
    
    # Маршруты для корзины
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # API маршруты
    path('api/', include(api_urlpatterns)),
] 