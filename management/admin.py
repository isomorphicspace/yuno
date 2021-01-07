from django.contrib import admin

from .models import Products

# Register your models here.


# class ProductAdmin(admin.ModelAdmin):
#     exclude = ('created_time', 'modified_time')
#     list_display = ('mainClass', 'name', 'model', 'price')
#     def save_model(self, request, obj, form, change):
#         obj.creator = request.user
#         super().save_model(request, obj, form, change)


# admin.site.register(Products, ProductAdmin)
admin.site.register(Products)