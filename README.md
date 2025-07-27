# TreeMenuTest

## Быстрый старт

1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Примените миграции, создайте суперюзера(если нужен доступ к админке джанго) и запустите сервер:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
3. Откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/) для просмотра меню. При применении миграций сгенерировались предзагруженные данные.

## Управление меню

Добавляйте пункты через стандартную админку Django [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).