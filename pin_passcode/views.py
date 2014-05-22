from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from django.middleware.csrf import get_token


@requires_csrf_token
def form(request):
    get_token(request)
    return render(request, 'pin_passcode/form.html')


def auth(request):
    if request.method == 'POST':
        pin = request.POST.get('pin', None)
        if pin == settings.PIN_PASSCODE_PIN:
            username = settings.PIN_PASSCODE_USERNAME

            if not username:
                username = 'admin'

            try:
                user = get_user_model().objects.get(username=username)
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                login(request, user)
                return HttpResponse(status=200)
            except get_user_model().DoesNotExist:
                pass


    return HttpResponse(status=401)
