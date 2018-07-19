from unittest import mock

from django.db import connection
from django.db.models.base import ModelBase
from django.db.utils import OperationalError
from django.test import TestCase
from linebot import LineBotApi
from linebot.models import MessageEvent

from linecms.models import Message, Task

BOT_MESSAGE_FLAG = object()
REPLY_TOKEN_FLAG = object()


# https://stackoverflow.com/a/51146819/9186433
class AbstractModelMixinTestCase(TestCase):
    mixin = None

    @classmethod
    def setUpTestData(cls):
        if not hasattr(cls, 'model'):
            cls.model = ModelBase('__TestModel__' + cls.mixin.__name__,
                                  (cls.mixin, ),
                                  {'__module__': cls.mixin.__module__})

        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls.model)
            super(AbstractModelMixinTestCase, cls).setUpClass()
        except OperationalError:
            pass

    @classmethod
    def tearDownClass(self):
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(self.model)
            super(AbstractModelMixinTestCase, self).tearDownClass()
        except OperationalError:
            pass


class SendMessageTaskTestCase(AbstractModelMixinTestCase):
    mixin = Task

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.mesg1 = Message.objects.create(
            message_type=Message.MESSAGE_TYPE_TEXT, text="Text")
        cls.task1 = cls.model.objects.create(
            task_type=Task.TASK_TYPE_SEND_MESSAGE, message=cls.mesg1)

    @mock.patch(
        'linecms.models.Message.build_linebot_message',
        return_value=BOT_MESSAGE_FLAG)
    def test_do_handle_event(self, _mock):
        linebot_api = mock.Mock(spec=LineBotApi)
        impl = self.task1.do_handle_event(
            MessageEvent(reply_token=REPLY_TOKEN_FLAG), linebot_api)

        impl()
        linebot_api.reply_message.assert_called_once_with(
            REPLY_TOKEN_FLAG, BOT_MESSAGE_FLAG)
