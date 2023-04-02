from django.db import models


class Product(models.Model):
    id = models.PositiveIntegerField('Product ID', unique=True, primary_key=True)
    photo = models.ImageField('Product Photo', upload_to='products/')
    name = models.CharField('Product Name', max_length=100)
    description = models.TextField('Product Description', blank=True)
    price = models.PositiveIntegerField('Product Price')
    created_at = models.DateTimeField('Product Created At')
    product_category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'products'


class Category(models.Model):
    id = models.PositiveIntegerField('Category ID', unique=True, primary_key=True)
    name = models.CharField('Category Name', max_length=100)
    description = models.TextField('Category Description', blank=True)
    created_at = models.DateTimeField('Category Created At')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'categories'

