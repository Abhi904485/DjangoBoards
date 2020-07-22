# Django Boards

## how to run project
* python manage.py runserver

## Installing Rabbitmq in mac
* brew install rabbitmq
* brew services start rabbitmq

## Installing redis in mac
* brew install redis
* brew services start redis

## how to run celery
`start one Worker node`
* celery -A DjangoBoards  worker -l info

`start flower feom celery for watching and monitoring`
* celery flower -A DjangoBoards --address=127.0.0.1 --port=555


`start beat from celery for chrontab or scheduled task`
* celery -A DjangoBoards  beat -l info

`start celery beat with custom schedulers`
* celery -A DjangoBoards  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler


## Necessary Rabbitmq Configurations

* rabbitmq-plugins enable rabbitmq_management

* rabbitmqctl add_user root root 

* rabbitmqctl set_user_tags root administrator

* rabbitmqctl add_vhost sample_host   

* rabbitmqctl set_permissions -p sample_host root ".*" ".*" ".*"

* Rabbitmq management page access url : http://localhost:15672/#/users/root
