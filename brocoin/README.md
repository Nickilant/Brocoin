# **Brocoin v1.0**

## Запуск бекенда brocoin:

#### Предусловия: Должен быть установлен Python версии не ниже 3.10 и актуальный Postgresql
1) Подготовка бд: Нужно создать базу данных и выполнить в ней скрипт из приложенного файла db.sql. Он создаст все необходимые таблицы и зависимости
2) В консоли перейти в директорию проекта \brocoin\ и выполнить команду 

    "_**pip install -r requirements.txt**_"
3) После установки всех пакетов нужно перейти в дирексторию brocoin\brocoin\, открыть файл
settings.py, на 75 строке найти настройки базы данных и подставить туда данные от нашей бд.
После чего вернуться в директорию brocoin\ и выполнить команду

    "_**python manage.py runserver**_"

    она запустит бекенд поекта Brocoin на локалхосте

## Api бекенда brocoin

##### На данный момент представлено 7 POST апи эндпоинтов
1) get/user/ - Получение данных о пользователе. Регистрация нового пользователя происходит автоматически по этому же апи, получение процентов с рефов здесь же
2) get/tasks/ - Получение списка заданий с пометкой выполнения
3) done/tasks/ - Помечает задание как выполненное
4) add/score/ - Добавляет очков пользователю
5) add/tickets/ - Добавляет тикеты пользователю
6) remove/score/ - Отнимает очки пользователя
7) remove/tickets/ - Отнимает тикеты пользователя

<<<<<<< HEAD
Описание типов возвращаемых данных:

get/user/ - Ответ приходит в формате json который содержит в себе следующие поля:

"username" - string,

"score" - int,

"last_tap" - datetime,

"referals" - json,

"ref_code" - string,

"position" - int,

"tickets" - int

Пример:

{
    "username": "antonprox",
    "score": 2937,
    "start_mining": "2024-08-20 11:47:51.000377",
    "referals": [
        {
            "username": "antonprox_ref",
            "refs": 0,
            "bonus": "5000"
        },
        {
            "username": "antonprox_ref1",
            "refs": 0,
            "bonus": 0
        },
        {
            "username": "antonprox_ref2",
            "refs": 0,
            "bonus": 0
        }
    ],
    "ref_code": "624161982",
    "position": 1,
    "tickets": 2
}


get/tasks - Ответ представляет собой массив содержащий json-ы со следующими полями:

"id" - int,

"description" - string,

"points" - int,

tickets - int,

duration - string ("infinity" - неограниченная)

"links" - string,

"complete" - bool

Пример:

{
    "tasks": [
        {
            "id": 1,
            "description": "Бро готовят задания",
            "points": 1000,
            "tickets": 0,
            "duration": "infinity",
            "links": "https://t.me/itsbrocoin",
            "complete": true
        },
        {
            "id": 2,
            "description": "Второе задание",
            "points": 5000,
            "tickets": 0,
            "duration": "infinity",
            "links": "https://t.me/itsbrocoin",
            "complete": true
        },
        {
            "id": 3,
            "description": "Subscribe my Channel",
            "points": 1000,
            "tickets": 0,
            "duration": "infinity",
            "links": "https://youtube.com",
            "complete": false
        }
    ]
}

v1.1 :

    Добавлена ручка сбора бенефитов с рефералов
    Добавлены поля duration и tickets в задания
    Переработано отображение рефералов в контексте по пользователю
    Переработан ответ с контекстом по заданиям
    Добавлена ручка запуска майнинга

