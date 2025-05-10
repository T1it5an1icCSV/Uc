from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review, Favorite, Discount

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'city', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('first_name', 'last_name', 'email')
    exclude = ('postal_code',)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity')
    raw_id_fields = ('order', 'product')
    list_filter = ['order']
    search_fields = ['order__id', 'product__name']

admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Discount)
