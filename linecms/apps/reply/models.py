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


class AbstractAction(models.Model):
    """Reply action."""

    class Meta:
        abstract = True

    REPLY_TEXT = 1
    REPLY_CHOICES = ((REPLY_TEXT, _("Text")), )

    reply = models.IntegerField(choices=REPLY_CHOICES)
    reply_text = models.ForeignKey(Text, on_delete=models.PROTECT)

    def handle_event(self, event, line_bot_api):
        providers = {
            self.REPLY_TEXT: self.reply_text,
        }

        provider = providers[self.reply]
        line_bot_api.reply_message(event.reply_token,
                                   provider.get_line_bot_object())
