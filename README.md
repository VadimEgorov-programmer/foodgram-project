# foodgram-project   

Ссылка на сайт https://diplom-vadimegorov-programmer.tk/

## Description

Foodgram-это сервис, который позволяет пользователям публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Любой авторизованный пользователь может добавить рецепт в "список покупок" и загрузить сводный список ингредиентов в виде PDF-файла.

## Getting Started

Эти инструкции помогут вам создать копию проекта и запустить его на локальном компьютере для целей разработки и тестирования.

### Prerequisites

Перед установкой необходимо убедиться, что в вашей системе установлена последняя версия Docker Desktop:

```
    docker --version
```

Если нет, установите его с помощью менеджера пакетов.

Ubuntu example:

```
    sudo apt-get update
    sudo apt-get remove docker docker-engine docker.io
    sudo apt install docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
```

### Installing and deployment

Вы можете просто клонировать этот репозиторий на локальную машину, создать файл '.env' с вашими локальными переменными (примеры вы можете найти ниже) и запустить "docker-compose up".

В противном случае выполните следующие шаги:

1. В каталоге проекта вам нужно создать файл dot-env со следующими переменными:

```
    # Django
    SECRET_KEY=<your-secret-key>

    # Postgres
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=<your_password>
    DB_HOST=db
    DB_PORT=5432
```

Если вы хотите использовать Django в режиме отладки, просто дополнительно добавьте "DEBUG=True", в противном случае не указывайте его вообще.

2. Затем создайте docker-compose.файл yaml.

Проект ("веб") в "сервисе" должен выглядеть следующим образом:

```
  ...

  web:
    image: vilagov/yamdb:latest
    volumes:
      - staticfiles:/code/static
    ports:
      - "8000:8000"
    depends_on: 
      - "db"
    env_file: 
      - ./.env
```

Также доступно изображение с поддержкой ARM.

3. Затем, наконец, создайте файл настроек nginx и назовите его "host.conf".
Он должен содержать /статические/ и /медиа/ местоположения.
Пример:

```
    server {
    listen 80;
    server_name 0.0.0.0;
    server_tokens off;

    location /static/ {
        alias /static/;
    }

    location /media/ {
        alias /media/;
    }

    location / {
        proxy_pass http://web:8000;
    }
    }
```

4. В конце концов, просто запустите docker-compose:

```
    docker-compose up
```
