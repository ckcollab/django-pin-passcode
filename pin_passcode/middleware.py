from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpResponseRedirect


class PinPasscodeMiddleware:
    def process_request(self, request):
        allowed_urls = [
            reverse('pin_form'),
            reverse('pin_auth'),
        ]
        try:
            allowed_urls.append(reverse('admin:index'))
        except NoReverseMatch:
            pass

        if request.path not in allowed_urls:
            pin_passcode_logged_in = request.session.get("pin_passcode_logged_in", None)
            if not request.user.is_authenticated() and not pin_passcode_logged_in:
                return HttpResponseRedirect("%s?next=%s" % (reverse('pin_form'), request.path))
