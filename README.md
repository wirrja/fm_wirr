### https://wirr.ru
 - username: demo
 - password: Password_demo#

[22mb] https://i.imgur.com/0zz7YHH.gif


### API:
POST:
https://wirr.ru/api/v1/scrobble

##### httpie:

$ http -a username:password URL <<< json

##### json:

    {

    "date_listen": 1522782052,

    "song": {
            "title": "Rocks in Pockets",
            "length": 360000    #ms
        },
    "album": {
            "title": "The Long Term Physical Effects Are Not Yet Known"
        },
    "artist": {
            "name": "Jay-Jay Johanson"
        }
    }
![screenshot](https://i.imgur.com/O2CJZWz.jpg)

#### fm_wirr/client
contains scrobble examples

## Dev environment
$ cd dir_which_contains_.git

$ pip3 install -r requirements.txt

### 4 open terminal windows
$ source venv/bin/activate

#### postgres & redis containers
- $ cd dev_docker
- $ docker-compose up

#### django
- $ python3 fm_wirr/manage.py collectstatic --settings=config.settings_local
- $ python3 fm_wirr/manage.py migrate --settings=config.settings_local
- $ python3 fm_wirr/manage.py createsuperuser --settings=config.settings_local
- $ python3 fm_wirr/manage.py runserver --settings=config.settings_local

#### celery-worker
- $ cd fm_wirr
- $ DJANGO_SETTINGS_MODULE='config.settings_local' celery -A config.celery_local worker -l info

#### celery-beat
- $ cd fm_wirr
- $ DJANGO_SETTINGS_MODULE='config.settings_local' celery -A config.celery_local beat -l info -S django

#### browser
- http://localhost:8000
- http://localhost:8000/admin
- http://localhost:8000/api/v1/


