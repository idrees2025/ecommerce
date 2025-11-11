from django.contrib import admin
from .models import Products,CartItem,productimage

class image(admin.TabularInline):
    model = productimage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [image]

admin.site.register(Products,ProductAdmin)
admin.site.register(CartItem)