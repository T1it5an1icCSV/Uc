from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Category, Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для работы с категориями товаров.
    GET /api/categories/ - получить список всех категорий
    GET /api/categories/{id}/ - получить детали категории
    POST /api/categories/ - создать новую категорию (только администратор)
    PUT /api/categories/{id}/ - обновить категорию (только администратор)
    DELETE /api/categories/{id}/ - удалить категорию (только администратор)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        """Разрешения: GET-запросы доступны всем, остальные - только админам"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API для работы с товарами.
    GET /api/products/ - получить список всех товаров
    GET /api/products/{id}/ - получить детали товара
    POST /api/products/ - создать новый товар (только администратор)
    PUT /api/products/{id}/ - обновить товар (только администратор)
    DELETE /api/products/{id}/ - удалить товар (только администратор)
    """
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        """Разрешения: GET-запросы доступны всем, остальные - только админам"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Фильтрация товаров"""
        queryset = Product.objects.filter(available=True)
        
        # Фильтрация по категории
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Поиск по имени товара
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        return queryset

class OrdersAPIView(APIView):
    """
    API для работы с заказами пользователя.
    GET /api/orders/ - получить список заказов пользователя
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def api_root(request):
    """Корневая точка API с описанием доступных эндпоинтов"""
    return Response({
        'categories': 'GET /api/categories/',
        'products': 'GET /api/products/',
        'orders': 'GET /api/orders/ (требуется аутентификация)',
        'documentation': 'API представляет доступ к каталогу товаров и заказам'
    }) 