from django.db import models
from django.utils.translation import gettext as _

from .message import Message


class Task(models.Model):
    """Task model."""

    class Meta:
        abstract = True

    TASK_TYPE_SEND_MESSAGE = 1
    TASK_TYPE_CHOICES = ((TASK_TYPE_SEND_MESSAGE, _("Send Message")), )
    task_type = models.IntegerField(_("Task type"), choices=TASK_TYPE_CHOICES)

    # send message
    message = models.ForeignKey(
        Message, on_delete=models.PROTECT, null=True, blank=True)

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
            return self._handlers[self.task_type]
        except KeyError as e:
            raise ValueError("Invalid task type: " + self.task_type) from e

    # Operations

    def do_handle_event(self, event, linebot_api):
        return self._get_handler().do_handle_event(self, event, linebot_api)


class AbstractHandler:
    @staticmethod
    def do_handle_event(model, event, linebot_api):
        raise NotImplementedError()


@Task.handler(Task.TASK_TYPE_SEND_MESSAGE)
class SendMessageTaskHandler(AbstractHandler):
    fields = ('message', )

    @staticmethod
    def do_handle_event(model, event, linebot_api):
        def _impl():
            linebot_api.reply_message(event.reply_token,
                                      model.message.build_linebot_message())

        return _impl
