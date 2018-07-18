from unittest import mock

from django.test import TestCase
from linebot.models import FollowEvent, ImageMessage, MessageEvent, TextMessage

from linecms.models import Task, TextMessageHook

TEST_FLAG = object()


class TextMessageHookTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        hook = TextMessageHook.objects.create(
            task_type=Task.TASK_TYPE_SEND_MESSAGE, keyword="test")

    @mock.patch('linecms.models.Task.do_handle_event', return_value=TEST_FLAG)
    def test_handle_event(self, _mock):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="test")), None)
        self.assertEqual(agent, TEST_FLAG)

    def test_handle_event_not_matching(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="coba")), None)
        self.assertEqual(agent, None)

    def test_handle_event_not_text_message(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=ImageMessage()), None)
        self.assertEqual(agent, None)

    def test_handle_event_not_message_event(self):
        agent = TextMessageHook.handle_event(FollowEvent(), None)
        self.assertEqual(agent, None)
