# Деплой сайта lesswrong.ru

Новый сайт (этот репозиторий) находится в разработке. Деплой будет настроен на адрес next.lesswrong.ru, пока этот репозиторий не будет готов к продакшну.

## Общая информация

* Сервер работает на Hetzner Cloud.
* DNS настроен в AWS через Route 53.
* Сервер настраивается с помощью ansible  в [этом репозитории](https://github.com/lesswrong-ru/lesswrong-ru).
* Деплой работает через GitLab CI. В GitLab для этого настроено [зеркало репозитория](https://gitlab.com/kocherga/lw/website).
* Контейнеры поднимаются с помощью docker-compose.
