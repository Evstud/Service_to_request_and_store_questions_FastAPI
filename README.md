# Service_to_request_and_store_questions_FastAPI
Сервис для получения и хранения вопросов с публичного API (https://jservice.io/api/random).
Приложение написано на FastAPI, в качестве БД используется PostgreSQL, при разработке применились SQLAlchemy, Docker, Docker-compose.
## Сборка и запуск
 
Для локального запуска приложения необходимо наличие установленного docker и docker-compose (для Linux: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru).
Затем необходимо клонировать репозиторий (в терминале: git clone 'git@github.com:Evstud/Service_to_request_and_store_questions_FastAPI.git')
Далее нужно перейти в директорию с файлами приложения, там должен быть файл 'docker-compose.yml', который нужно запустить в  терминале с помощью команды 'docker-compose up -d'.
После этого произойдет создание образов и запуск контейнеров с приложением и БД.
Проверить запущено ли приложение можно с помощью терминала и команд 'docker ps' и т.д. 
Или с помощью интерфейса Swagger на который можно зайти c помощью ввода в адресной строке браузера 'http://127.0.0.1:8001/docs#/'.
Для отправки запросов в приложение можно использовать:
1. Файл 'test_sender.py', находящийся в директории с файлами приложения. Предварительно на 16 строчке файла в аргументах функции 'send_questions_num()' необходимо указать количество вопросов для получения.
Далее в терминале нужно ввести команду 'python3 test_sender.py'. Произойдет отправка сообщения, в ответ придет список с уникальным/уникальными для данной БД вопросом/вопросами, сохраненными в БД. 
2. Http запрос, направленный на 'http://127.0.0.1:8001/questions_num/' с содержимым вида {'questions_num': integer} в формате json, где integer необхдимо заменить на количество вопросов. Пример запроса с помощью curl:
```
curl -X 'POST' \
  'http://127.0.0.1:8001/questions_num/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "questions_num": 5
}'
```
3. Интерфейс Swagger, в котором в группе методов 'Question' есть метод post, в котором необходимо указать количество вопросов.

## Описание приложения и БД
В БД выло создано 2 таблицы: 'Request' и 'Question'. Между ними - связь one-to-many. В связи с этим для 'Request' были разработаны методы:
- Get Requests (для получения списка всех запросов),
- Delete Request By Id (для удаления запроса по id).
Для 'Question' были разработаны методы:
- Main (для отправки количества вопросов, получения вопросов, регистрации экземпляров в таблицах 'Request' и 'Question'),
- Get Questions (для получения списка всех вопросов),
- Get Questions By Request Id (для получения вопросов, относящихся к определенному запросу (по id запроса)),
- Delete Request (для удаления вопроса по id).
В БД сохраняются только уникальные вопросы (которых еще нет в БД), при получении неуникальных вопросов отправляется повторный запрос на публичный API.
