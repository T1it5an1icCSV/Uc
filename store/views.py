from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Category, Product, Order, OrderItem
from django.contrib import messages
from decimal import Decimal
from django.conf import settings

# Вспомогательная функция для создания сессии корзины, если она не существует
def get_cart(request):
    """Вспомогательная функция для создания сессии корзины, если она не существует"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def index(request):
    """Главная страница магазина."""
    categories = Category.objects.all()[:6]
    products = Product.objects.filter(available=True).order_by('-created')[:8]
    return render(request, 'store/index.html', {
        'categories': categories,
        'products': products,
    })

class CategoryListView(ListView):
    """Список всех категорий."""
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    """Детальная информация о категории с товарами."""
    model = Category
    template_name = 'store/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            category=self.object, available=True
        )
        return context

class ProductListView(ListView):
    """Список всех товаров."""
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    """Детальная информация о товаре."""
    model = Product
    template_name = 'store/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем похожие товары той же категории
        context['related_products'] = Product.objects.filter(
            category=self.object.category, 
            available=True
        ).exclude(id=self.object.id)[:4]
        return context

def cart_add(request, product_id):
    """Добавление товара в корзину."""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_cart(request)
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1, 
            'price': str(product.price)
        }
    
    # Явно сохраняем изменения в сессии
    request.session.modified = True
    
    # Выводим сообщение о добавлении товара в корзину для отладки
    print(f"Товар {product.name} добавлен в корзину. Текущая корзина: {cart}")
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect('store:cart_detail')

def cart_remove(request, product_id):
    """Удаление товара из корзины."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session.modified = True
        messages.success(request, f'Товар "{product.name}" удален из корзины.')
    
    return redirect('store:cart_detail')

def cart_detail(request):
    """Просмотр корзины."""
    cart = get_cart(request)
    cart_items = []
    total_price = Decimal('0')
    
    # Отладочная информация
    print(f"Содержимое корзины: {cart}")
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, available=True)
            price = Decimal(item_data['price'])
            quantity = item_data['quantity']
            total_item_price = price * quantity
            total_price += total_item_price
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': total_item_price
            })
            
            # Отладочная информация
            print(f"Добавлен товар в отображение: {product.name}, {quantity} шт., {price} руб.")
            
        except Product.DoesNotExist:
            # Если продукт удален или недоступен, удаляем его из корзины
            del cart[product_id]
            request.session.modified = True
            print(f"Удален недоступный товар из корзины: ID {product_id}")
    
    # Отладочная информация
    print(f"Общее количество товаров в корзине: {len(cart_items)}")
    print(f"Общая стоимость: {total_price}")
    
    return render(request, 'store/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def order_create(request):
    """Создание нового заказа."""
    cart = get_cart(request)
    
    # Если корзина пуста - перенаправляем на страницу корзины
    if not cart:
        messages.warning(request, 'Ваша корзина пуста!')
        return redirect('store:cart_detail')
    
    cart_items = []
    total_price = Decimal('0')
    
    # Получаем товары из корзины
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, available=True)
            price = Decimal(item_data['price'])
            quantity = item_data['quantity']
            total_item_price = price * quantity
            total_price += total_item_price
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': total_item_price
            })
        except Product.DoesNotExist:
            del cart[product_id]
            request.session.modified = True
    
    if request.method == 'POST':
        # Обработка формы заказа
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code', '')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        note = request.POST.get('note', '')
        
        # Создаем заказ
        if request.user.is_authenticated:
            user = request.user
        else:
            # Для анонимных пользователей используем суперпользователя или создаем гостевой аккаунт
            from django.contrib.auth.models import User
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                # Если нет суперпользователя, создаем его
                user = User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin'
                )
        
        # Создаем заказ без postal_code
        order = Order(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            city=city,
            phone=phone,
            note=note
        )
        # Если поле существует в базе, устанавливаем его
        try:
            order.postal_code = postal_code
        except:
            pass
        
        order.save()
        
        # Создаем элементы заказа для каждого товара в корзине
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        # Очищаем корзину
        request.session['cart'] = {}
        request.session.modified = True
        
        # Отправляем пользователя на страницу подтверждения заказа
        return redirect('store:order_complete', order_id=order.id)
    
    return render(request, 'store/order_create.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def order_complete(request, order_id):
    """Страница подтверждения заказа."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_complete.html', {'order': order})

@login_required
def order_history(request):
    """История заказов пользователя."""
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Детали конкретного заказа."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
