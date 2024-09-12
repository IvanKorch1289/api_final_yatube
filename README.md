# api_final_yatube

# Описание:

Финальный проект спринта: API для Yatube.
Устанавливает эндпоинты API к сервису Yatube.


# Примеры запросов к API:

1. Получить список всех публикаций. При указании параметров limit и offset выдача должна работать с пагинацией:

GET http://127.0.0.1:8000/api/v1/posts/

Ответ:

    {
    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
    "results": [
                {
                "id": 0,
                "author": "string",
                "text": "string",
                "pub_date": "2021-10-14T20:41:29.648Z",
                "image": "string",
                "group": 0
            }
        ]
    }
    

2. Добавление новой публикации в коллекцию публикаций. Анонимные запросы запрещены.

POST http://127.0.0.1:8000/api/v1/posts/

Тело запроса:
    {
        "text": "string",
        "image": "string",
        "group": 0
    }

Ответы:

Статус ответа 201
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2019-08-24T14:15:22Z",
        "image": "string",
     
    }

Статус ответа 400
    {
        "text":
        [
            "Обязательное поле."
        ]
    }

Сатус ответа 401

    {
    "detail": "Учетные данные не были предоставлены."
    }

Подробно ознакомиться с документацией можно по адресу: http://<адрес_хоста>/redoc/