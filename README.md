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

Telegram-бот-магазин написан на языке программирования Python. Используя фреймворки, такие как Django и Aiogram. Есть админ-панель Django с возможностью создавать/редактировать/удалять категории, подкатегории, товары, пользователей. Сам бот имеет систему регистрации, функцию входа в учетную запись и сброса пароля. Пароли пользователей хэшируются и не поддаются никаким изменениям. Администратор не сможет изменить имя пользователя и пароль пользователя. Только пользователь сможет сбросить свой пароль и сменить его на новый. После входа в систему пользователь получит доступ к таким командам, как справка, описание, каталог. Когда вы нажмете команду каталог, перед ним появится встроенная клавиатура с категорией товаров, после выбора категории появится встроенная клавиатура с подкатегориями, и после этого он увидит товары. Существуют также команды для администратора, такие как рассылка пользавателям телеграмм бота. Также были созданы обработчики незнакомых, непонятных команд и сообщений для бота. Используется база данных Postgresql
___________
## Инструкция
### 1. Установка библиотек
- Скопируйте репозиторий:
`git clone https://github.com/dosmukhambetov/DjangoAiogram_TelegramStoreBot/ && cd django_aiogram`

- Установить библиотеки:
`pip install -r requirements.txt`

### 2. Поменять базу данных, TOKEN_API телеграмм бота, ID администратора телеграмм бота, SECRET_KEY Django
- Переименуйте файл `.env.example` на `.env`
- Измените TOKEN_ID, SECRET_KEY, ADMIN_ID, PG_NAME, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT внутри `django_aiogram/bot_file/.env/`

### 3. Сделайте миграции
- Перейдите сюда `cd django_aiogram/`
- Напишите эти команды:
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py createsuperuser`

### 4. Запуск бота
- Чтобы запустить Django напишитите** `python manage.py runserver`
- Чтобы запустить телеграмм бота напишите** `python manage.py bot`
___________
## Функционал телеграмм бота
- В боте есть такие команды как
`Регистрация, Вход, Забыли пароль, Помощь, Описание, Каталог и Меню Администратора и т.д.`
Снизу показан пример работы бота ⬇️
### 1. Команды авторизации (Регистрация, Вход, Забыли пароль)
<p><img src="https://i.ibb.co/wYq9bWp/Group-1-1.png", alt="authentification"></p>

Здесь реализована система регистрации, входа в профиль. Есть функция забыли пароль. При созданий пароля, пароль хешируется. Пользователь может создать только один профиль. Потому что его ID пользователя уже будет присвоена к профилю при регистрации. Команда 'Регистрация' сперва запрашивает логин, пототм, идет проверка, есть ли уже такой логин у других пользователей, если есть, то он попросит ввести новый(уникальный логин), а если логин который он ввел доступен для использования, то уже идет создание пароля. Пароль должен содержать как минимут одну цифру, и быть только из латинских букв. Если, пользователь создал некорректный пароль то ему скажут каким должен быть пароль. После чего как он создал пароль, пароль хешируется, и пользователь сохраняется в базе данных и отображается в Django админ панели. У администратора нет никаких возможностей редактировать данные пользователя

### 2. Команда каталог(Категории, Подкатегории, Товары)
<p><img src="https://i.ibb.co/JtCVDzb/view-products-3.png", alt="view products"></p>

Команда каталог, которая отвечает за показ категории, подкатегории и товаров. Команда каталог доступна только лишь тогда, когда пользователь вошел в профиль(выполнил вход). На изоброжении показана как работает эта команда. Могут быть случаи когда в категории или в подкатегории нет товаров, то тогда бот скажет что в этой категории/подкатегории нет товаров. Здесь категории, подкатегории и товары сортируются по мере их добавления. А сами эти объекты можно добавлять, редактировать и удалять в админ панели Django

### 3. Дефолтные команды (Помощь, Описание, Админ -> Рассылка)
<p><img src="https://i.ibb.co/BGmCShZ/default-commands-1.png", alt="default commands"></p>

Здесь сделаны дефолтные команды, такие как 'Помощь', которая предостовляет помощь по боту. Есть команда 'Описание', это описание телеграмм магазина/бота. Так же есть и интересная команда называемая 'Админ'. Чтобы пользователь мог использовать эту команду ему нужно быть в списке телеграмм администраторов. После нажатия на эту кнопку, вас перекинет на меню администратора. В котором сейчас 1 команда 'Рассылка: ' и кнопки такие как домой, и помощь. Кнопка помощь отвечает за инструкцию администратора, его команды и т.д. Кнопка домой просто возвращает его на главное меню. Благодаря команде 'Рассылка: ' администратор можем отправить сообщение всем зарегистрированым пользователям данного телеграмм бота
___________
## Django панель Администратора:
- С помощью Django сделаны модели, админ панель, связи между моделями и многое другое.
### 1. Простая домашняя страница
<p><img src="https://i.ibb.co/DzDrD9t/5.png", alt="simple main page"></p>

**Самая простая, которая только есть, домашняя страница (html + bootstrap).** С простым и кратким описанием проекта

___________
### 2. Панель Администратора:
<p><img src="https://i.ibb.co/8s5YnGP/5-1.png", alt="admin panel"></p>

___________
### 3. Продкуты (Товары) в Админке:
<p><img src="https://i.ibb.co/2F44czw/1-7.png", alt="creating_product"></p>
<p><img src="https://i.ibb.co/KqrST0P/1-3.png", alt="products_list"></p>

Продукт (Товар), принимает фотографию, название, описание, цену, опубликован ли он, а также, категорию и подкатегорию. Подкатегория связана с категорией. В Django админ панели отображаются все созданные товары

___________
### 4. Категории в Админке:
<p><img src="https://i.ibb.co/j5jqyP5/2-2.png", alt="creating_category"></p>
<p><img src="https://i.ibb.co/XYQNxZ4/img.png", alt="categories_list"></p>

Категория, принимает название и описание. В Django админ панели отображаются все созданные категории

___________
### 5. Подкатегории в Админке:
<p><img src="https://i.ibb.co/y0dWFKc/1-4.png", alt="creating_subcategory"></p>
<p><img src="https://i.ibb.co/hypGJFz/1-5.png", alt="subcategories_list"></p>

Подкатегория, принимает название подкатегории, описание подкатегории и также Категорию. В Django админ панели отображаются все созданные подкатегории

___________
### 6. Пользователи телеграмм бота в Админке:
<p><img src="https://i.ibb.co/C5p57QM/1-8.png", alt="user"></p>
<p><img src="https://i.ibb.co/dprc2w1/1-9.png", alt="users_list"></p>

Пользователь, принимает ID пользователя, логин, пароль, и зарегистрирован ли он. Пользователь создается в телеграмм боте. И данные как ID пользователя и зарегистрирован ли он получаются автоматически. В Django админ панели отображаются пользователи которые зарегистрированы в телеграмм боте. Администратор не имеет возможности редактировать данные пользователей. Пароли пользователей хешируются

___________
