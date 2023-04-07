from django.db import models


class Product(models.Model):
    photo = models.ImageField(verbose_name='Фотография', upload_to='products/')
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', blank=False)
    price = models.PositiveIntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время редактирования', auto_now=True)
    is_published = models.BooleanField(verbose_name='Опубликован', default=True)
    product_category = models.ForeignKey(verbose_name='Категория', to='Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'products'
        ordering = ['-created_at']


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', blank=True)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'
        ordering = ['-created_at']

