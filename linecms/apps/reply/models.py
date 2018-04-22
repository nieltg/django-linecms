from django.db import models
from django.utils.translation import gettext as _
from linebot.models import TextSendMessage


class Text(models.Model):
    """LINE text message model."""

    text = models.TextField(_('Text'), max_length=2000)

    def get_line_bot_object(self):
        return TextSendMessage(text=self.text)

    def __str__(self):
        return self.text[:100]
