from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.http import HttpResponseRedirect


class PinPasscodeMiddleware:
    def process_request(self, request):
        # First check if we're on a whitelisted IP in which case we can ignore all of this
        if hasattr(settings, 'PIN_PASSCODE_IP_WHITELIST'):
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                # Get heroku IPs specially (behind routers and stuff, this special field
                # passes client IPs)
                ip_adds = request.META['HTTP_X_FORWARDED_FOR'].split(",")
                ip = ip_adds[0]
            else:
                # Get regular IPs
                ip = request.META['REMOTE_ADDR']
            if ip in settings.PIN_PASSCODE_IP_WHITELIST:
                return

        # Check that we're on a blocked (not allowed) page
        allowed_urls = [
            reverse('pin_form'),
            reverse('pin_auth'),
        ]
        try:
            allowed_urls.append(reverse('admin:index'))
        except NoReverseMatch:
            # No admin urls could be found, ignore
            pass

        if request.path not in allowed_urls:
            pin_passcode_logged_in = request.session.get("pin_passcode_logged_in", None)
            if not request.user.is_authenticated() and not pin_passcode_logged_in:
                return HttpResponseRedirect("%s?next=%s" % (reverse('pin_form'), request.path))
