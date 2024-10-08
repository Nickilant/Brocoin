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

##### На данный момент представлены следующие POST апи эндпоинтоы
1) get/user/ - Получение данных о пользователе. Регистрация нового пользователя происходит автоматически по этому же апи, получение процентов с рефов здесь же
2) get/tasks/ - Получение списка заданий с пометкой выполнения
3) done/tasks/ - Помечает задание как выполненное
4) add/score/ - Добавляет очков пользователю
5) add/tickets/ - Добавляет тикеты пользователю
6) remove/score/ - Отнимает очки пользователя
7) remove/tickets/ - Отнимает тикеты пользователя
8) get/referals/ - Получение рефералов пользователя
9) switch_region/ - Изменение региона(изменение языка в аппке)
10) check/task/ - проверка выполнения задания для таски 


Описание типов возвращаемых данных:

check/task/ - ответ приходит в формате json

{'complete_task': 'True'} - True если условия выполнены, False если нет 


get/user/ - Ответ приходит в формате json который содержит в себе следующие поля:

"username" - string,

"score" - int,

"left_mining" - datetime,

"mining_claim" - bool,

"ref_code" - string,

"position" - int,

"tickets" - int

"daily_stric" - int

"daily_calim" - bool

"boxes" - int

"region" - string

"first_game" - bool

"first_login" - bool

"advertising_limit" - int

"advertising_total" - int

"ton_balanse" - int

"push_see" - bool (true если посмотрел, false если нет)

Пример:


    "username": "antonprox",
    "score": 31222,
    "left_mining": "00:00",
    "mining_claim": true,
    "ref_code": "624161982",
    "position": 1,
    "tickets": 165,
    "boxes": 0,
    "daily_stric": 1,
    "daily_claim": False
    "first_login": false,
    "region": "ru",
    "first_game": true
    "advertising_limit": 10,
    "advertising_total": 10,
    "ton_balanse": 0.41



get/tasks - Ответ представляет собой массив содержащий json-ы со следующими полями:

"id" - int,

"description" - string,

"points" - int,

tickets - int,

duration - string ("infinity" - неограниченная)

"links" - string,

"complete" - bool

"priority" - int (1 если приоритетная, 2 если нет)

"region" - string (eng, ru и тд если региональная, universal если для всех)



Пример:


    "tasks": [
        {
            "id": 1,
            "description": "Бро готовят задания",
            "points": 1000,
            "tickets": 0,
            "duration": "infinity",
            "links": "https://t.me/itsbrocoin",
            "complete": true,
            "priority": 2,
            "region": "universal"
        },
        {
            "id": 2,
            "description": "Второе задание",
            "points": 5000,
            "tickets": 0,
            "duration": "infinity",
            "links": "https://t.me/itsbrocoin",
            "complete": true,
            "priority": 2
            "region": "ru"
        },
        {
            "id": 3,
            "description": "Subscribe my Channel",
            "points": 1000,
            "tickets": 0,
            "duration": "infinity",
            "links": "https://youtube.com",
            "complete": false,
            "priority": 2
            "region": "eng"
        }
    ]


get/referals - Получение рефералов пользователя

"username" - string

"referals" - массив json

"total_referals" - int

Пример

    "username": "antonprox",
    "referals": [
        {
            "username": "antonprox_ref",
            "refs": 0,
            "bonus": "5000",
            "reward": 0
        },
        {
            "username": "antonprox_ref1",
            "refs": 0,
            "bonus": 0,
            "reward": 0
        }
    ],
    "total_referals": 6,
    "total_pages": 3,
    "current_page": 1,
    "total_score": 11000


v1.1 :

    Добавлена ручка сбора бенефитов с рефералов
    Добавлены поля duration и tickets в задания
    Переработано отображение рефералов в контексте по пользователю
    Переработан ответ с контекстом по заданиям
    Добавлена ручка запуска майнинга

