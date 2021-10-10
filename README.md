![example workflow](https://github.com/DariaDolotina/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# praktikum_new_diplom
Foodgram - сервис для публикации рецептов. 
Функционал:
- создание и редактирование рецептов;
- подписка на авторов;
- добавление рецептов в избранное;
- добавление рецептов в корзину;
- выгрузка списка ингредиентов для покупки.

Подготовка и запуск проекта:

- cклонируйте репозиторий;
- на удалённом сервере установите docker и docker-compose;
- локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP;
- скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер;
- на сервере создайте .env файл и впишите:
    - DB_ENGINE=<django.db.backends.postgresql>
    - DB_NAME=<имя базы данных postgres>
    - DB_USER=<пользователь бд>
    - DB_PASSWORD=<пароль>
    - DB_HOST=<db>
    - DB_PORT=<5432>
    - SECRET_KEY=<секретный ключ проекта django>
- для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    - DB_ENGINE=<django.db.backends.postgresql>
    - DB_NAME=<имя базы данных postgres>
    - DB_USER=<пользователь бд>
    - DB_PASSWORD=<пароль>
    - DB_HOST=<db>
    - DB_PORT=<5432>
    - DOCKER_PASSWORD=<пароль от DockerHub>
    - DOCKER_USERNAME=<имя пользователя>
    - SECRET_KEY=<секретный ключ проекта django>
    - USER=<username для подключения к серверу>
    - HOST=<IP сервера>
    - PASSPHRASE=<пароль для сервера, если он установлен>
    - SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
  
- на сервере соберите docker-compose и примените миграции:
  1. sudo docker-compose -f docker-compose.yml up -d
  2. sudo docker-compose exec -T web python manage.py makemigrations
  3. sudo docker-compose exec -T web python manage.py migrate --noinput
  
  Проект доступен по адресу:
  
  http://62.84.119.45/
  
  

