FROM python:3.11-alpine

# Устанавливаем системные зависимости для mysqlclient
RUN apk add --no-cache \
    build-base \
    mariadb-dev \
    pkgconfig \
    bash

WORKDIR /app

COPY requirements.txt .

# Обновляем pip (иногда критично)
RUN pip install --upgrade pip

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

ENV ENV=docker

CMD ["gunicorn", "SDG_for_buisness.wsgi:application", "--bind", "0.0.0.0:8000"]

