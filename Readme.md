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


## Django Management Commands

*  python manage.py squashmigrations --squashed-name accounts_migration accounts start_migration_file_name end_migration_file_name

        for ex:  
        1. python manage.py squashmigrations --squashed-name accounts_migration accounts 0001_initial 0002
        2. python manage.py squashmigrations --squashed-name boards_migration boards 0001_initial 0002 
        
*  python manage.py collectstatic
        
        for ex:
        1. For collecting All static files into static root dir confogured in setting.py that will use in production.
        
*   python manage.py findstatic md/simplemde.min.js
         
        for ex:
        1.Found 'md/simplemde.min.js' here:   /Users/akumars1/Downloads/python_project/Django_projects/DjangoBoards/static/md/simplemde.min.js

*   python manage.py check

        for ex:
        1.System check identified no issues (0 silenced).
        

*   python manage.py showmigartions

        accounts
          [X] 0001_accounts_migration (2 squashed migrations)
        boards
          [X] 0001_boards_migration (2 squashed migrations)
          
*   python manage.py sqlmigrate boards 0001_boards_migration

       ###### Before Running python manage.py migrate command you can check what query will execute on Db migrate .

       app_lable = boards
       
       migration_name  =  0001_boards_migration

        BEGIN;
        --
        -- Create model Board
        --
        CREATE TABLE "board" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE, "description" varchar(500) NOT NULL);
        --
        -- Create model Topic
        --
        CREATE TABLE "topic" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "subject" varchar(50) NOT NULL UNIQUE, "last_updated" datetime NOT NULL, "board" integer NOT NULL REFERENCES "board" ("id") DEFERRABLE INITIALLY DEFERRED, "user" integer NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED, "views" integer unsigned NOT NULL CHECK ("views" >= 0));
        --
        -- Create model Post
        --
        CREATE TABLE "post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "message" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NULL, "created_by" integer NOT NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED, "topic" integer NOT NULL REFERENCES "topic" ("id") DEFERRABLE INITIALLY DEFERRED, "updated_by" integer NULL REFERENCES "user" ("id") DEFERRABLE INITIALLY DEFERRED);
        CREATE INDEX "topic_board_c61853e5" ON "topic" ("board");
        CREATE INDEX "topic_user_d49faade" ON "topic" ("user");
        CREATE INDEX "post_created_by_57ea8c18" ON "post" ("created_by");
        CREATE INDEX "post_topic_f73323a0" ON "post" ("topic");
        CREATE INDEX "post_updated_by_5c8817c5" ON "post" ("updated_by");
        COMMIT;

*   python manage.py sqlflush
        
       ###### it will return list of sql statements which is required for DB Flush
 
 
        BEGIN;
        DELETE FROM "user";
        DELETE FROM "user_user_permissions";
        DELETE FROM "django_celery_results_taskresult";
        DELETE FROM "django_celery_beat_clockedschedule";
        DELETE FROM "topic";
        DELETE FROM "auth_group";
        DELETE FROM "django_session";
        DELETE FROM "user_groups";
        DELETE FROM "django_celery_beat_periodictask";
        DELETE FROM "django_admin_log";
        DELETE FROM "auth_group_permissions";
        DELETE FROM "post";
        DELETE FROM "django_content_type";
        DELETE FROM "django_celery_beat_solarschedule";
        DELETE FROM "django_celery_beat_periodictasks";
        DELETE FROM "auth_permission";
        DELETE FROM "board";
        DELETE FROM "django_celery_beat_crontabschedule";
        DELETE FROM "django_celery_beat_intervalschedule";
        UPDATE "sqlite_sequence" SET "seq" = 0 WHERE "name" IN ('user', 'user_user_permissions', 'django_celery_results_taskresult', 'django_celery_beat_clockedschedule', 'topic', 'auth_group', 'django_session', 'user_groups', 'django_celery_beat_periodictask', 'django_admin_log', 'auth_group_permissions', 'post', 'django_content_type', 'django_celery_beat_solarschedule', 'django_celery_beat_periodictasks', 'auth_permission', 'board', 'django_celery_beat_crontabschedule', 'django_celery_beat_intervalschedule');
        COMMIT;

*   python manage.py flush

        Removes ALL DATA from the database, including data added during migrations. Does not achieve a "fresh install" state.

*   python manage.py dbshell 
        
        SQLite version 3.33.0 2020-08-14 13:23:32
        Enter ".help" for usage hints.
        sqlite> .help
        
*   python manage.py inspectdb > all_models.py

        For Existing DB if we want to create models. so we can use 
        
        
*   python manage.py dumpdata --indent 4 boards -o boards.json
*   python manage.py dumpdata --indent 4 accounts -o  accounts.json

*   python manage.py loaddata --indent 4 accounts -o  accounts.json
*   python manage.py loaddata --indent 4 boards -o boards.json

        for ex:
        
            (django_rest_swagger) akumars1@C02Z2EC7LVCG DjangoBoards % python manage.py loaddata boards.json
            Installed 41 object(s) from 1 fixture(s)
            (django_rest_swagger) akumars1@C02Z2EC7LVCG DjangoBoards % python manage.py loaddata accounts.json
            Installed 2 object(s) from 1 fixture(s)


*   python manage.py  diffsettings

        for ex:
            Displays differences between the current settings.py and Django's default settings.
