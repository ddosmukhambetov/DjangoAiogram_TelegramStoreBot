from django.db import models
from smart_selects.db_fields import ChainedForeignKey


# Создаем модели нашего приложения
class TelegramUser(models.Model):
    chat_id = models.IntegerField(verbose_name='ID пользователя', unique=True, null=True)
    user_login = models.CharField(verbose_name='Логин', max_length=255, unique=True)
    user_password = models.CharField(verbose_name='Пароль', max_length=128)
    is_registered = models.BooleanField(verbose_name='Зарегистрирован', default=False)
    registered_at = models.DateTimeField(verbose_name='Время регистрации', auto_now_add=True)

    def __str__(self):
        return self.user_login

    class Meta:
        verbose_name = 'Телеграмм Пользователь'
        verbose_name_plural = 'Телеграмм Пользователи'
        db_table = 'telegram_users'
        ordering = ['-registered_at']


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


class SubCategory(models.Model):
    name = models.CharField(verbose_name='Название подкатегории', max_length=100)
    description = models.TextField(verbose_name='Описание подкатегории', blank=True)
    created_at = models.DateTimeField(verbose_name='Время создания подкатегории', auto_now_add=True)
    subcategory_category = models.ForeignKey(verbose_name='Категория', to='Category', on_delete=models.PROTECT,
                                             null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        db_table = 'subcategories'
        ordering = ['-created_at']


class Product(models.Model):
    photo = models.ImageField(verbose_name='Фотография', upload_to='products/')
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', blank=False)
    price = models.PositiveIntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время редактирования', auto_now=True)
    is_published = models.BooleanField(verbose_name='Опубликован', default=True)
    product_category = models.ForeignKey(verbose_name='Категория', to='Category', on_delete=models.PROTECT, null=True)

    # ChainedForeignKey Для работы с зависимыми полями (наша подкатегория зависима от категории). Smart Selects
    # Документация django-smart-selects https://django-smart-selects.readthedocs.io/en/latest/
    product_subcategory = ChainedForeignKey(
        to=SubCategory,
        chained_field='product_category',
        chained_model_field='subcategory_category',
        show_all=False,
        auto_choose=True,
        null=True,
        verbose_name='Подкатегория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'products'
        ordering = ['-created_at']
