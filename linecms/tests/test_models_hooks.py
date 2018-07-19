from unittest import mock

from django.test import TestCase
from linebot.models import FollowEvent, ImageMessage, MessageEvent, TextMessage

from linecms.models import Task, TextMessageHook


def pk_from_do_handle_event(self, _event, _linebot_api):
    return self.pk


class TextMessageHookTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hook1 = TextMessageHook.objects.create(
            task_type=Task.TASK_TYPE_SEND_MESSAGE, keyword="test")

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="test")), None)
        self.assertEqual(agent, self.hook1.pk)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event_not_matching(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="coba")), None)
        self.assertEqual(agent, None)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event_not_text_message(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=ImageMessage()), None)
        self.assertEqual(agent, None)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event_not_message_event(self):
        agent = TextMessageHook.handle_event(FollowEvent(), None)
        self.assertEqual(agent, None)


class TextMessageHookCaseSensitiveTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hook1 = TextMessageHook.objects.create(
            task_type=Task.TASK_TYPE_SEND_MESSAGE,
            keyword="test",
            case_sensitive=True)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="test")), None)
        self.assertEqual(agent, self.hook1.pk)

    @mock.patch('linecms.models.Task.do_handle_event',
                lambda self, _event, _linebot_api: self.pk)
    def test_handle_event_not_matching(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="Test")), None)
        self.assertEqual(agent, None)


class TextMessageHookCaseSensitivePriorityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hook1 = TextMessageHook.objects.create(
            task_type=Task.TASK_TYPE_SEND_MESSAGE, keyword="test")
        cls.hook2 = TextMessageHook.objects.create(
            task_type=Task.TASK_TYPE_SEND_MESSAGE,
            keyword="Test",
            case_sensitive=True)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="test")), None)
        self.assertEqual(agent, self.hook1.pk)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event_no_case_matches(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="TEST")), None)
        self.assertEqual(agent, self.hook1.pk)

    @mock.patch('linecms.models.Task.do_handle_event', pk_from_do_handle_event)
    def test_handle_event_case_sensitive_matches(self):
        agent = TextMessageHook.handle_event(
            MessageEvent(message=TextMessage(text="Test")), None)
        self.assertEqual(agent, self.hook2.pk)
