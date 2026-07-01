## Обновление Docker-образа и публикация в Docker Hub
``` Сборка нового Docker-образа
docker build -t analytics-service:latest .
```
``` Запушить образ
docker push chilivardev/analytics-service:latest
```

## Обновление контейнера на сервере
```
docker pull chilivardev/analytics-service:latest
```

## Перезапуск проекта 
```
docker compose down
docker compose up -d
```
--- Полный сброс базы данных (удалит все данные) ---
```
docker compose down -v
docker compose up -d
```


