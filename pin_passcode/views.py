from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import requires_csrf_token
from django.middleware.csrf import get_token


@requires_csrf_token
def form(request):
    get_token(request)
    return render(request, 'pin_passcode/form.html')


@requires_csrf_token
def auth(request):
    if request.method == 'POST':
        received_pin = request.POST.get('pin', None)
        actual_pin_code = getattr(settings, 'PIN_PASSCODE_PIN', None)
        if not actual_pin_code:
            raise Exception("PIN_PASSCODE_PIN setting not set!")
        next_page = request.GET.get('next', '/')

        if received_pin == str(actual_pin_code):
            username = getattr(settings, 'PIN_PASSCODE_USERNAME', None)
            if username:
                try:
                    user = get_user_model().objects.get(username=username)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return HttpResponse(status=200)
                except get_user_model().DoesNotExist:
                    raise Exception("User %s not found!" % username)
            else:
                # No username defined, so let's just set a flag in the session
                request.session["pin_passcode_logged_in"] = True
                return HttpResponseRedirect(next_page)
        else:
            return HttpResponse(status=401)

def test(request):
    '''This view is just for testing, you shouldn't be able to get to it unless
    you are authed from django or PIN PASSCODE'''
    return HttpResponse()
