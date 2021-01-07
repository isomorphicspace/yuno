from django.db import models

# Create your models here.

ProductLevel = [
    (0, "A"),
    (1, "B"),
    (2, "C"),
    (3, "S")
]


class Products(models.Model):
    main_class = models.CharField(max_length=30, blank=False, verbose_name="主类")
    name = models.CharField(max_length=30, blank=False, verbose_name="名称")
    model = models.CharField(max_length=30, blank=False, verbose_name="型号")
    price = models.FloatField(blank=False, verbose_name="市场价")
    cost = models.FloatField(blank=False, verbose_name="成本价")
    sub_class = models.CharField(max_length=30, blank=True, verbose_name="子类")
    brand = models.CharField(max_length=30, blank=True, verbose_name="品牌")
    suppiler = models.CharField(max_length=30, blank=True, verbose_name="供应商")
    inner_model = models.CharField(max_length=30, blank=True, verbose_name="内部型号")
    unit = models.CharField(max_length=5, blank=True, verbose_name="单位")
    picture = models.CharField(max_length=100, blank=True, verbose_name="图片")
    product_page = models.CharField(max_length=100, blank=True, verbose_name="产品页")
    introduce = models.TextField(max_length=300, blank=True, verbose_name="简介")
    link = models.CharField(max_length=100, blank=True, verbose_name="链接")
    level = models.SmallIntegerField(blank=True, choices=ProductLevel, verbose_name="产品等级")
    inventory = models.IntegerField(blank=True, null=True, verbose_name="库存")
    note = models.TextField(max_length=300, blank=True, verbose_name="备注")
    created_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    modified_time = models.DateField(auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = u'products'
        verbose_name = u'产品'
        verbose_name_plural = u'产品'

    def __str__(self):
        return self.main_class

