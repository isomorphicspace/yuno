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
export_products_to_csv.allowed_permissions = ('export',)


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

    # 可以设置根据不同用户详情返回不同的字段，比如这里可以设计成，采购可以先登录设置好产品名称、型号和成本等敏感信息，
    # 然后由其他不能接触到成本的用户来录入其他的信息
    # def get_fieldsets(self, request, obj=None):

    # 限制数据集，没有设置此方法，则返回全部数据集
    # def get_queryset(self, request):

    # readonly_fields = ('name', 'model', 'cost',)
    # list_editable = ('price',)
    # def save_model(self, request, obj, form, change):
    #     obj.creator = request.user
    #     super().save_model(request, obj, form, change)

    # 当前用户是否有导出权限：
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'group1' in group_names:
            return ['price']
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(ProductAdmin, self).get_changelist_instance(request)

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        logger.info('group_names:{}'.format(group_names))
        return group_names

    def get_readonly_fields(self, request, obj=None):
        groups = self.get_group_names(request.user)
        if 'group1' in groups:
            logger.info("user:{} in group1".format(request.user.username))
            return ['name', 'model', 'cost']
        return ()


admin.site.register(Products, ProductAdmin)
