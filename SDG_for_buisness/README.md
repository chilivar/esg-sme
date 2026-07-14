## Клонирование репозитория с подмодулями

* Для клонирования полного репозитория пропишите в консоли следующую команду:
```bash
  git clone --recurse-submodules https://github.com/DrakeNeJivoy/SDG_portal
```
* В случае если вы уже склонировали репозиторий без флага --recurse-submodules, то вам нужно прописать следующие команды:
```bash
  git submodule update --init --recursive
```

## Запуск проекта

- Для запуска проекта необходимо прописать в консоли команду:
  ```bash
  docker-compose up -d --build
  ```

- При изменении кода в вашем сервисе, чтоб не пересобирать все сервисы, можно указать конкретный сервис:
  ```bash
  docker-compose up -d --build <service_name>
  ```

- Ручной запуск для разработки:
  ```bash
  python manage.py runserver 0.0.0.0:8001 --settings SDG_for_buisness.dev
  ```
  
- Запуск локальной сборки docker
  ```bash
  docker-compose -f docker-compose.local.yml up -d --pull always --build
  ```

- После полной соборки вы можете обратиться к сервису по адресу:
  ```
  http://localhost:<Порт вашего сервиса в docker-compose.yml>
  ```