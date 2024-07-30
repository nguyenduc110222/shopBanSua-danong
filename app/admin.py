from django.contrib import admin
from app.models import*
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Slider)
admin.site.site_header = "Shop Sữa Đàn Ông"