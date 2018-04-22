from django.db import models
from django.utils.translation import gettext as _

from linecms.apps.reply.models import AbstractAction


class Postback(AbstractAction):
    """Postback message."""

    data = models.TextField(_("Postback data"), max_length=300)

    def __str__(self):
        return self.data


class Message(AbstractAction):
    """Reply message."""

    text = models.CharField(_("Keyword text"), max_length=255)

    def __str__(self):
        return self.text


class InvalidMessage(AbstractAction):
    """Invalid message."""
