from custom_models import User
from rest_framework.response import Response
from django.utils.translation import ugettext, ugettext_lazy as _


def check_email_exists(backend, details, uid, user=None, *args, **kwargs):
    print 'Check Email Verify ', user

    email = details.get('email', '')
    provider = backend.name

    # check if social user exists to allow logging in (not sure if this is
    # necessary)
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    print 'Check Email Verify social ', social
    # check if given email is in use
    count = User.objects.filter(email=email).count()
    print 'Check Email Verify count ', count
    # user is not logged in, social profile with given uid doesn't exist
    # and email is in use
    if not user and not social and count:
        return Response({'message': _("Email is ready in system. Please choice another email.")}, status=400)
