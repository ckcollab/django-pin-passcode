import django

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

# Have to do settings here before importing models
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'pin_passcode',
    ),
    ROOT_URLCONF='pin_passcode.urls',
    PIN_PASSCODE_PIN=1234,
)
django.setup()

from django.contrib.auth.models import AnonymousUser, User

from .middleware import PinPasscodeMiddleware
from .views import auth


class PinPasscodeMiddlewareTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='password'
        )
        self.middleware = PinPasscodeMiddleware()

    def test_pin_passcode_wrong_does_not_redirect(self):
        request = self.factory.get(reverse("pin_test"))
        request.user = AnonymousUser()
        request.session = {}
        response = self.middleware.process_request(request)
        assert response.status_code == 302
        assert response.url == "/pin/?next=/pin/test"

    def test_pin_passcode_incorrect_pin_returns_401_response(self):
        request = self.factory.post(
            "%s?next=%s" % (reverse("pin_auth"), reverse("pin_test")),
            {"pin": "0"}  # wrong passcode
        )
        request.user = AnonymousUser()
        request.session = {}
        response = self.middleware.process_request(request)
        assert response is None  # middleware didn't have to do anything, this view is allowed
        response = auth(request)
        assert response.status_code == 401

    def test_pin_passcode_correct_pin_redirects_and_sets_session(self):
        request = self.factory.post(
            "%s?next=%s" % (reverse("pin_auth"), reverse("pin_test")),
            {"pin": "1234"}
        )
        request.user = AnonymousUser()
        request.session = {}
        response = self.middleware.process_request(request)
        assert response is None  # middleware didn't have to do anything, this view is allowed
        response = auth(request)
        assert response.status_code == 302
        assert response.url == "/pin/test"

    def test_pin_passcode_recognizes_logged_in_user(self):
        request = self.factory.get(reverse("pin_test"))
        request.user = self.user
        request.session = {}
        response = self.middleware.process_request(request)
        assert response is None  # No redirect response sent

    def test_pin_passcode_recognizes_session_variable(self):
        request = self.factory.get(reverse("pin_test"))
        request.user = AnonymousUser()
        request.session = {"pin_passcode_logged_in": True}
        response = self.middleware.process_request(request)
        assert response is None  # No redirect response sent

    def test_pin_passcode_allows_certain_urls(self):
        request = self.factory.get(reverse('pin_form'))
        request.user = AnonymousUser()
        request.session = {}
        response = self.middleware.process_request(request)
        assert response is None  # Lets us use this page to input pin

        request = self.factory.get(reverse('pin_auth'))
        request.user = AnonymousUser()
        request.session = {}
        response = self.middleware.process_request(request)
        assert response is None  # Lets us use this page to auth pin

    def test_pin_passcode_allows_certain_ips(self):
        # This should work, our local ip
        with self.settings(PIN_PASSCODE_IP_WHITELIST=('127.0.0.1',)):
            request = self.factory.get('/')
            request.user = AnonymousUser()
            request.session = {}
            response = self.middleware.process_request(request)
            assert response is None

        # Remove IP whitelist, shouldn't work any more
        request = self.factory.get('/')
        request.user = AnonymousUser()
        request.session = {}
        response = self.middleware.process_request(request)
        assert response.status_code == 302
