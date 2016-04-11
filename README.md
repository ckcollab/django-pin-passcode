django-pin-passcode [![Circle CI](https://circleci.com/gh/ckcollab/django-pin-passcode.svg?style=svg)](https://circleci.com/gh/ckcollab/django-pin-passcode)
===================

<p align="center"><img src="https://github.com/ckcollab/django-pin-passcode/raw/master/docs/screenshot.png" alt="Django Pin Passcode Example"></p>

This is a simple app that adds a site wide pin-passcode for quick authentication. I wrote this originally for my personal
motivation tracker [chin up](https://github.com/ckcollab/chin-up) so I could quickly login from my phone.

You enter a PIN passcode (using 0-9 and #, can use numpad) until the correct pin is entered, then:
 
 * If `PIN_PASSCODE_USERNAME` is set, you will be logged in as this user

 * Otherwise, a session variable will be set and you will be able to browse the site



Installation
============

```bash
pip install django-pin-passcode
```


```python
# settings.py

INSTALLED_APPS += (
    'pin_passcode',
)

...

MIDDLEWARE_CLASSES += (
    'pin_passcode.middleware.PinPasscodeMiddleware',
)

...

# user to sign in as, omit this option to use a session variable instead
# PIN_PASSCODE_USERNAME = 'eric' # uncomment this to login as "eric" after valid pin code is entered

# the passcode required to login as the above user, using 0-9 and '#' 
PIN_PASSCODE_PIN = 1234
        
# IP addresses to give access to automatically
PIN_PASSCODE_IP_WHITELIST = ('123.123.123.123',)
```


```python
# urls.py

urlpatterns = patterns(
    ...
    url(r'^', include('pin_passcode.urls')),
    ...
)
```


Testing
=======

`pip install -r requirements.txt`

`py.test`
