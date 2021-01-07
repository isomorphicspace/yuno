from django.contrib import admin

from .models import Products

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('main_class', 'name', 'model', 'price')
    fieldsets = (['必填', {'fields': ('main_class', ('name', 'model'), ('price', 'cost')), }],
                 ['选填', {'fields': ('sub_class', 'brand', 'supplier', 'inner_model', 'unit', 'picture',
                                    'product_page', 'introduce', 'link', 'level', 'inventory', 'note'),
                         'classes': ('collapse',)}])
#     def save_model(self, request, obj, form, change):
#         obj.creator = request.user
#         super().save_model(request, obj, form, change)


admin.site.register(Products, ProductAdmin)
