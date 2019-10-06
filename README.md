# Новый сайт LessWrong.ru

Пишем новый LessWrong.ru на Django и Wagtail.

## Как запускать

Команды ниже отсылают к Makefile. Если у вас не установлен `make`, вы можете брать строчки из Makefile и запускать соответствующие команды вручную.

### Docker way

1. `make dev` - поднимает docker-образы через docker-compose (django-приложение и mysql-базу). При запуске контейнер `app` будет поначалу выдавать ошибки (пока запускается база), это нормально.
2. `make db_setup` - создаёт таблицы.

### Без Docker

Если у вас есть Docker, лучше пользуйтесь им - описанный ниже способ использует sqlite-базу вместо mysql, что может привести к будущим багам при деплое.

1. Убедитесь, что у вас установлен python3.7.
2. Сделайте virtualenv: `python3 -mvenv venv`
3. Активируется virtualenv: `. ./venv/bin/activate`
4. Установите зависимости: `pip install -r ./requirements.txt`
5. Переключите django settings: `export DJANGO_SETTINGS_MODULE=lw.core.settings.dev_sqlite`
6. Запустите проект: `./manage.py runserver 8020`
7. Заполните базу: `./manage.py migrate`
