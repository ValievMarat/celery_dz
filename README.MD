# Домашнее задание к лекции "Celery"

## Запуск проекта
Для запуска необходимо:
1. установить зависимости:

pip install -r requirements.txt

2. Запустить redis (через docker-compose):

docker-compose up

3. Запустить celery:

celery -A tasks.app worker --pool=eventlet --loglevel=INFO

использовал флаг pool==eventlet для запуска на windows

4. запустить app.py для запуска Flask

5. Создать в корне папку Files (если не создана), используется для сохранения входящих файлов

6. Запустить примеры запросов requests_examples.py
В результате работы итоговый файл сохраняется в корень как result_file.png