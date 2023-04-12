from django.apps import AppConfig


class BotFileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_file'

    # verbose_name отображение в Django админке
    verbose_name = 'Продукты'
