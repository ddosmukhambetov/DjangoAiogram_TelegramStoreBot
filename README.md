# DjangoAiogram_TelegramStoreBot
___________
<p align="center">
  <img src="https://i.ibb.co/5MZTwRh/banner.png" alt="Project Banner" width="726">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3x-yellow", alt="Python Version">
  <img src="https://img.shields.io/badge/aiogram-2.25.1-blue", alt="Aiogram Version">
  <img src="https://img.shields.io/badge/Django-4.2-success", alt="Django Version">
</p>

___________
## О проекте:

Telegram-бот-магазин написан на языке программирования Python. Используя фреймворки, такие как Django и Aiogram. Есть админ-панель Django с возможностью создавать/редактировать/удалять категории, подкатегории, товары, пользователей. Сам бот имеет систему регистрации, функцию входа в учетную запись и сброса пароля. Пароли пользователей хэшируются и не поддаются никаким изменениям. Администратор не сможет изменить имя пользователя и пароль пользователя. Только пользователь сможет сбросить свой пароль и сменить его на новый. После входа в систему пользователь получит доступ к таким командам, как справка, описание, каталог. Когда вы нажмете команду каталог, перед ним появится встроенная клавиатура с категорией товаров, после выбора категории появится встроенная клавиатура с подкатегориями, и после этого он увидит товары. Существуют также команды для администратора, такие как рассылка пользавателям телеграмм бота. Также были созданы обработчики незнакомых, непонятных команд и сообщений для бота. Используется база данных Postgresql.
___________
## Инструкция
### 1. Установка библиотек
- **Скопируйте репозиторий:**
**`git clone https://github.com/dosmukhambetov/DjangoAiogram_TelegramStoreBot/ && cd django_aiogram`**

- **Установить библиотеки:**
**`pip install -r requirements.txt`**

### 2. Поменять базу данных, TOKEN_API телеграмм бота, ID администратора телеграмм бота, SECRET_KEY Django
- **Поменяйте базу данных в **`django_aiogram/config/settings/`****
<p align="left"><img src="https://i.ibb.co/60CZ8yP/db.png", alt="Change DB"></p>

- **Переименуйте файл **`.env.example`** на **`.env`****
- **Измените TOKEN_ID, SECRET_KEY, ADMIN_ID в **`django_aiogram/bot_file/.env/`****

<p align="left"><img src="https://i.ibb.co/6YrGx1M/2023-04-13-011719.png", alt="Change TOKEN_API, ADMIN_ID, SECRET_KEY"></p>

### 3. Сделайте миграции
- **Перейдите сюда** **`cd django_aiogram/`**
- **Напишите эти команды:**
**`python manage.py makemigrations`**
**`python manage.py migrate`**
**`python manage.py createsuperuser`**
___________
## Телеграмм бот
