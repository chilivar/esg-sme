## Запуск проекта
Склонировать этот проект
```
 git clone https://github.com/chilivar/NEWS_DB.git
```
ПЕРЕД НАЧАЛОМ УБЕДИТЬСЯ ЧТО DOCKER ВКЛЮЧЕН!!!

Чтобы запустить сервис нужно перейти в этот проект в консоле и прописать эту команду
```
docker compose up -d --pull always --force-recreate
```

Перед работой с сервисом нужно записать данные в бд
## Заполнение БД 
```В postman сделать GET запрос
http://localhost:8081/api/parser/sources/all
```
Должен вернуться ответ 200 ОК

## Получить основные данные
```
http://localhost:8083/api/news/impacts
```

## Если хотите остановить и очистить данные в БД 
```
docker compose down -v
```

## phpMyAdmin
```
http://localhost:8082/index.php
```

## SWAGGER
Analytics-service
```
http://localhost:8083/swagger-ui/index.html#/
```
news-parser-service
```
http://localhost:8081/swagger-ui/index.html#/
```
