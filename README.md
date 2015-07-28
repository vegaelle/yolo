# YALA

Yet Another Learning Assistant, a learning management system written in Django.

## Requirements

YALA is written in Python3, and does not plan to support Python2 for now
(although it could come later). Its only real requirement is Django-1.8 (but
some optional Django dependencies are also required, like Pillow or PyYAML).

You may need the following system-wide libs (for example if you run a
Debian-Like system):

- python3-dev (for Pillow)
- libjpeg-dev (for thumbnails support)
- libpng-dev (for thumbnails support)
- libpq-dev (for Psycopg2 support, if you intend to use Postgresql)

## Setup

1. Install Virtualenv, if you don’t have it yet

    pip install --user virtualenv

2. Create a virtualenv with Python3

    virtualenv -p /usr/bin/python3 yala_env

3. Activate this virtualenv

    source ./yala_env/bin/activate

4. Clone repository, and get in the project dir

    git clone https://github.com/gordon-/yala && cd yala

5. Install project dependencies

    pip install -r requirements.txt


## Run in debug mode

The provided `settings.py` is sufficient for debug purposes. In development
environment, you can work with a SQLite database. Get in the project
repository, and type:

    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

Optionnally, you can load some fixtures as demo data, with this command:

    ./manage.py loaddata tests

## Run in production

In production, you are adviced to use a Postgresql database. From the Django
root , copy `yala/localsettings.py.example` to `yala/localsettings.py`, and
edit the content of the new file. Then, type:

    ./manage.py collectstatic
    ./manage.py migrate
    ./manage.py createsuperuser

The production environment also have more dependencies, so, instead of
installing `requirements.txt`, you should type this:

    pip install -r requirements-prod.txt

The Django app is ready to serve. You now have to make it run with the supplied
Gunicorn, one way or another. We suggest `supervisor`, and [this nice guide (in
french)](http://www.miximum.fr/deployer-django-en-production-nginx-gunicorn-supervisor.html) 
that clearly explains how to install all of this.

Don’t forget to statically serve the `staticfiles` dir under the `/static/` URL,
in your virtualhost!
