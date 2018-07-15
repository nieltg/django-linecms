from django.db import models
from django.utils.translation import gettext as _
from linebot.models import TextSendMessage


class Message(models.Model):
    """LINE message model."""

    MESSAGE_TYPE_GROUP = 0
    MESSAGE_TYPE_TEXT = 1
    MESSAGE_TYPE_CHOICES = (
        (MESSAGE_TYPE_GROUP, _("Message Group")),
        (MESSAGE_TYPE_TEXT, _("Text Message")),
    )
    message_type = models.IntegerField(
        _("Message type"), choices=MESSAGE_TYPE_CHOICES)

    # group
    items = models.ManyToManyField(
        'self', verbose_name=_("Group Items"), blank=True)
    # text
    text = models.TextField(_("Text"), max_length=2000, null=True, blank=True)

    # Handlers

    _handlers = {}

    @classmethod
    def handler(cls, type_id):
        def _impl(handler_cls):
            if type_id in cls._handlers:
                raise ValueError(
                    "Handler for '{0}' is already defined".format(type_id))
            cls._handlers[type_id] = handler_cls

        return _impl

    def _get_handler(self):
        try:
            return self._handlers[self.message_type]
        except KeyError as e:
            raise ValueError("Invalid message type: " +
                             self.message_type) from e

    # Operations

    def build_linebot_message(self):
        return self._get_handler().build_linebot_message(self)

    def __str__(self):
        return self._get_handler().to_str(self)


class AbstractHandler:
    @staticmethod
    def build_linebot_message(model):
        raise NotImplementedError()

    @staticmethod
    def to_str(model):
        raise NotImplementedError()


@Message.handler(Message.MESSAGE_TYPE_GROUP)
class GroupMessageHandler(AbstractHandler):
    fields = ('items', )

    @staticmethod
    def build_linebot_message(model):
        queryset = model.items.all()
        if queryset.count() > 5:
            raise ValueError("Group items can't be more than 5")

        items = []
        for item in queryset:
            if item.message_type == Message.MESSAGE_TYPE_GROUP:
                raise ValueError("Group can't be nested")
            items.append(item.build_linebot_message())

        return items

    @staticmethod
    def to_str(model):
        return _("Group: %(id)s") % {'id': model.pk}


@Message.handler(Message.MESSAGE_TYPE_TEXT)
class TextMessageHandler(AbstractHandler):
    fields = ('text', )

    @staticmethod
    def build_linebot_message(model):
        return TextSendMessage(model.text)

    @staticmethod
    def to_str(model):
        return _("Text: %(text)s") % {'text': model.text}
