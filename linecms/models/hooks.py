from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from linebot.models import MessageEvent, TextMessage

from ..router import Router
from .task import Task

router = Router()


@router.put
class TextMessageHook(Task):
    """Text message hook model."""

    keyword = models.TextField(_("Keyword"), max_length=2000)

    case_sensitive = models.BooleanField(_("Case sensitive"), default=False)

    @classmethod
    def handle_event(cls, event, linebot_api):
        if not isinstance(event, MessageEvent):
            return None
        if not isinstance(event.message, TextMessage):
            return None

        keyword = event.message.text.strip()

        queryset = cls.objects.filter(
            Q(keyword=keyword, case_sensitive=True)
            | Q(keyword__iexact=keyword, case_sensitive=False)).order_by(
                '-case_sensitive')[:1]

        try:
            task = queryset.get()
        except ObjectDoesNotExist:
            return None

        return task.do_handle_event(event, linebot_api)

    def __str__(self):
        return self.keyword
