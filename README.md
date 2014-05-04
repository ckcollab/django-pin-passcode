django-pin-password
===================

![Django Pin Passcode Example](screenshot.png)

This is a simple app that adds a site-wide pin-passcode for quick authentication. I wrote this originally for my personal
motivation tracker called [chin up](https://github.com/ckcollab/chin-up) so I could quickly login from my phone.

You enter a PIN passcode (using 0-9 and #) and when you have entered the correct pin you will be logged in as `PIN_PASSCODE_USERNAME`
and forwarded either the index or the page you were trying to request.


Installation
============

Django Settings:

```python
INSTALLED_APPS += (
    'pin_passcode',
)
```

```python
MIDDLEWARE_CLASSES += (
    'pin_passcode.middleware.PinPasscodeMiddleware',
)
```

```python
PIN_PASSCODE_USERNAME = 'eric' # user to sign in as, defaults to "admin"
PIN_PASSCODE_PIN = 1234        # the passcode required to login as the above user, using 0-9 and #
```

Add to `urls.py`:

```python
url(r'^admin/', include(admin.site.urls)),
```
