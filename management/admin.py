from django.contrib import admin
from django.http import HttpResponse

from .models import Products
from datetime import datetime

import csv
import logging

logger = logging.getLogger(__name__)

# Register your models here.


# 定义导出动作
def export_products_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = ('main_class', 'name', 'model', 'price', 'cost', 'sub_class', 'brand', 'supplier',
                  'inner_model', 'unit', 'picture', 'product_page', 'introduce', 'link', 'level',
                  'inventory', 'note')
    response['Content-Disposition'] = 'attachment; filename={}_list_{}.csv'.format(
        'product',
        datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
    )

    # 定义表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
        logger.error("export products records. handler: {}, number: {}".format(request.user.username, len(queryset)))
    return response


export_products_to_csv.short_description = u'导出为csv文件'
# export_products_to_csv.allowed_permissions = ('export',)


class ProductAdmin(admin.ModelAdmin):
    actions = (export_products_to_csv, )
    list_display = ('main_class', 'name', 'model', 'price')
    list_filter = ('main_class', 'brand', 'supplier')
    search_fields = ('main_class', 'name', 'model', 'sub_class', 'brand', 'supplier', 'inner_model', 'level')
    ordering = ('main_class', 'sub_class', 'brand', 'name')
    fieldsets = (['必填', {'fields': ('main_class', ('name', 'model'), ('price', 'cost')), }],
                 ['选填', {'fields': ('sub_class', 'brand', 'supplier', 'inner_model', 'unit', 'picture',
                                    'product_page', 'introduce', 'link', 'level', 'inventory', 'note'),
                         'classes': ('collapse',)}])
#     def save_model(self, request, obj, form, change):
#         obj.creator = request.user
#         super().save_model(request, obj, form, change)


admin.site.register(Products, ProductAdmin)
