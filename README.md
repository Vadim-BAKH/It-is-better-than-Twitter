# It-is-better-than-Twitter
Diploma PET project FAST API


## Описание проекта
Проект представляет собой веб-приложение, построенное с использованием FastAPI, Nginx и PostgreSQL. Он организован по архитектурному паттерну MVC, что позволяет разделить логику приложения на три основные компоненты: модели, представления и контроллеры.


### Структура проекта

*fast_api/: Основная папка приложения, содержащая логику бизнес-уровня и взаимодействие с базой данных.*

    app.py: Точка входа в приложение, запускает сервер FastAPI.
    register_routes.py: Регистрация маршрутов (эндпоинтов) API.
    database.py: Модуль для взаимодействия с базой данных PostgreSQL.
    logs.py: Логирование событий и ошибок приложения.
    business_model/: Содержит модели таблиц и сервисы для работы с базой данных.
    factories/: Сопутствующие фабрики для создания объектов.
    schemas/: Схемы сериализации и валидации данных с использованием Pydantic.
    secret_mission/: Конфигуратор переменных окружения
    templates/: HTML-шаблоны для представления данных.

*nginx/: Конфигурация и файлы для Nginx, который будет использоваться как обратный прокси-сервер.*

    nginx.conf: Конфигурационный файл Nginx.
    Dockerfile: Dockerfile для создания образа Nginx.
    static/: Папка для статических файлов (CSS, JS, изображения и т.д.).

*tests/: Папка с тестами, написанными с использованием pytest для проверки функциональности приложения.*

*requirements.txt: Список зависимостей Python, необходимых для работы приложения.*

*supervisord.conf: Конфигурационный файл для Supervisor, который управляет процессами приложения.*

*Dockerfile: Dockerfile для создания образа приложения.*

*docker-compose.yml: Файл для настройки и запуска многоконтейнерного приложения с использованием Docker Compose.*

**Архитектура MVC**

    *Model (Модель):*
        Содержится в папке business_model/, где определяются модели таблиц и бизнес-логика для работы с данными.
        database.py отвечает за взаимодействие с базой данных PostgreSQL.

    *View (Представление):*
        HTML-шаблоны находятся в папке templates/, которые используются для отображения данных пользователю.
        Статические файлы (CSS, JS, JPG) находятся в папке static/ в папках css/, js/, medias/ в nginx/.

    *Controller (Контроллер):*
        app.py и register_routes.py обрабатывают входящие запросы, вызывают соответствующие модели и возвращают представления.
        Логика обработки запросов и маршрутизация находятся в register_routes.py.


### Установка

**Поготовка**

Создать рабочую директорию для проекта, установить виртуальное окружение.
*bash: python3 -m venv .myenv*
*bash: source .myenv/bin/activate*

**Скачивание HTTPS**

*bash: git clone https://github.com/Vadim-BAKH/It-is-better-than-Twitter.git

**Скачивание SSH**

*bash: git clone git@github.com:Vadim-BAKH/It-is-better-than-Twitter.git

**Секретные переменные**

*создать файл .env c указанием:*

     DB_USER=ваш логин
     
     DB_PASSWORD=ваш пароль


### Работа с приложением

#### Запуск и отключение

**Первый запуск**

*bash: docker compose up --build -d

**Отключене**

*bash: docker compose down*

**Следующий запуск**

*bash: docker compose up -d*

**Отключение с удалением базы данных**

*bash: docker compose down -v*

**Корректно работает приложение**
![image](https://github.com/user-attachments/assets/0c2cb508-7a22-45b5-adc8-9375b2158e9c)

**Диаграмма таблиц**




#### Тестировние
Приложение протестировано с использованием пайплайна CI/CD на GitHub Actions.
Для тестирования используется независимая база данных Posgresql и фич dependency_overrides от fastapi
для переопределения сессий с основной на тестовую

**Тестирование конфигурации приложения**

*bash: pytest -m config*
![image](https://github.com/user-attachments/assets/6a86d7d0-67b1-46d1-85b3-e7b7f4f25cbd)


**Полное тестирование работы приложения**

*bash: pytest -m app*
![image](https://github.com/user-attachments/assets/1e12586d-7b8c-4a5b-adef-33e623a300bb)

**Общий тест**

*bash: pytest -v*


#### Процесс работы приложения

__FastAPI-Swagger UI__

*Документация находится по адресу: http://http://127.0.0.1:8000/docs*

В докуметации отражена логика работы с данными. В том числе, перед работой в самом 
приложении необходимо создать пользователей. Для этого в форме запроса необходимо указать
только "name": "api_key" создаётся атоматически с технологией uuid и sha256:
![image](https://github.com/user-attachments/assets/7d6b085a-8a7b-462a-84e0-8250c7e2e744)
Так же можно просмотреть всех пользователей:
![image](https://github.com/user-attachments/assets/df9d6028-7842-4528-a9ca-a8e50e36d8c9)

__twitter-clone__

*Приложение работает по адресу:  http://http://localhost/api*

**Функционал приложения**

Главная страница работает только после создания первого пользователя.
Создаёт твит без медиа:
![image](https://github.com/user-attachments/assets/29bb9b9d-eedc-451e-b261-1c2b3cd3e8ff)
![image](https://github.com/user-attachments/assets/4f659cc0-9359-4210-a48a-4c093b6ffc38)
Создаёт твит с медиа:
![image](https://github.com/user-attachments/assets/eec7eb79-2a5f-4de5-ab0a-1c8db5bbde23)
![image](https://github.com/user-attachments/assets/e6435796-5bec-4718-96ff-f28fcdd4f387)
Ставит и удаляет лайки:
![image](https://github.com/user-attachments/assets/1d209ccf-d750-4ebc-8bf0-0cded273c7ea)
Показывает ленту твитов с приоритетом по количеству лайков:
![image](https://github.com/user-attachments/assets/0b57f77c-b080-45fb-ab6d-0589bd45cd9f)
![image](https://github.com/user-attachments/assets/6f91f965-b439-4550-8ba7-fde51ea30fae)
Позволяет заходить в профиль, подписаться на пользователя и отписаться от пользователя:
![image](https://github.com/user-attachments/assets/fefbb31b-b99a-47ea-80f0-01352b844253)
Открывает свой профиль:
![image](https://github.com/user-attachments/assets/4fe032cf-f8d0-405c-bc9d-d2479b640a06)


### Права
**Права принадлежат народу**
     
