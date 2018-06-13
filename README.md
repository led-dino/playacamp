# PlayaCamp

[![Build Status](https://travis-ci.org/led-dino/playacamp.svg?branch=master)](https://travis-ci.org/led-dino/playacamp)

A Django app for managing a Burning Man camp

## Running Locally

Make sure you have Python 3 [installed properly](http://install.python-guide.org).

```sh
$ git clone git@github.com:led-dino/playacamp.git
$ cd playacamp

$ pip install -r requirements.txt

$ python manage.py migrate

$ python manage.py runserver

# In another terminal
$ python manage.py livereload
```

You should also edit your `/etc/hosts` file to add an entry for `local.leddino.com`:

```
# /etc/hosts
127.0.0.1   local.leddino.com
```

Your app should now be running on [local.leddino.com:8000](http://local.leddino.com:8000/).

## Deploying to Heroku

When you land a change on the `master` branch it will automatically be deployed to a Heroku staging application.

## Documentation

