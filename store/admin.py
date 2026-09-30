from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem

# Admin Site Header Customization
admin.site.site_header = "SmashPoint Pro Store — Administration"
admin.site.site_title = "SmashPoint Admin Portal"
admin.site.index_title = "Equipment & Inventory Management"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Total Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumbnail',
        'name',
        'brand',
        'category',
        'formatted_price',
        'badge',
        'rating',
        'is_featured'
    ]
    list_display_links = ['image_thumbnail', 'name']
    list_filter = ['category', 'brand', 'is_featured', 'badge']
    list_editable = ['is_featured']
    search_fields = ['name', 'brand', 'specs', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

    fieldsets = (
        ("General Details", {
            'fields': ('category', 'name', 'slug', 'brand', 'price', 'is_featured')
        }),
        ("Badminton Technical Specifications", {
            'fields': ('specs', 'badge', 'rating', 'description')
        }),
        ("Product Media", {
            'fields': ('image_url', 'current_image_preview'),
        }),
    )

    readonly_fields = ['current_image_preview']

    def formatted_price(self, obj):
        return f"₹{int(obj.price):,}"
    formatted_price.short_description = "Price (INR)"
    formatted_price.admin_order_field = 'price'

    def image_thumbnail(self, obj):
        if obj.image_url:
            url = obj.image_url if obj.image_url.startswith('http') else f"/static/{obj.image_url}"
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: contain; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 2px;" />',
                url
            )
        return "No Image"
    image_thumbnail.short_description = "Visual"

    def current_image_preview(self, obj):
        if obj.image_url:
            url = obj.image_url if obj.image_url.startswith('http') else f"/static/{obj.image_url}"
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 6px;" />',
                url
            )
        return "No image specified"
    current_image_preview.short_description = "Image Preview"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'item_total']

    def item_total(self, obj):
        return f"₹{int(obj.price * obj.quantity):,}"
    item_total.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'full_name', 'phone_number', 'city', 'payment_method', 'formatted_total', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_id', 'full_name', 'phone_number', 'address', 'city', 'pincode']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id', 'created_at', 'total_amount']

    def formatted_total(self, obj):
        return f"₹{int(obj.total_amount):,}"
    formatted_total.short_description = "Order Total (INR)"
