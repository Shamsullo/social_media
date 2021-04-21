from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in
from django.core.signals import request_started


class CustomUser(AbstractUser):
    last_request = models.DateTimeField(_('last request'), blank=True, null=True)


def update_last_request_send(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    print('\n\n\n\n\n')
    print('*'*100)
    print('Sender:', sender)
    print('*'*100)
    print('User:', user)
    print('\n\n\n\n\n')

    # user.last_login = timezone.now()
    # user.save(update_fields=['last_login'])
request_started.connect(update_last_request_send)
