### https://wirr.pro
 - username: demo
 - password: Password_demo#

<img src="https://media.giphy.com/media/932H5rY7tC3RwkZBS8/giphy.gif" width="720" />

### API:
POST:
/api/v1/scrobble

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

#### fm_wirr/client
contains examples how to scrobble

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


