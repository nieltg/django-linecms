from django.test import TestCase
from linebot.models import TextSendMessage

from linecms.models import Message


class TextMessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        message = Message.objects.create(
            message_type=Message.MESSAGE_TYPE_TEXT, text="Text")
        cls.pk = message.pk

    def test_message_type(self):
        message = Message.objects.get(pk=self.pk)
        self.assertEqual(message.message_type, Message.MESSAGE_TYPE_TEXT)

    def test_build_linebot_message(self):
        message = Message.objects.get(pk=self.pk)
        bot_msg = message.build_linebot_message()

        self.assertIsInstance(bot_msg, TextSendMessage)
        self.assertEqual(bot_msg, TextSendMessage("Text"))


class GroupMessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        message = Message.objects.create(
            message_type=Message.MESSAGE_TYPE_GROUP)
        message.items.add(
            Message.objects.create(
                message_type=Message.MESSAGE_TYPE_TEXT, text="1"),
            Message.objects.create(
                message_type=Message.MESSAGE_TYPE_TEXT, text="2"))
        cls.pk = message.pk

    def test_message_type(self):
        message = Message.objects.get(pk=self.pk)
        self.assertEqual(message.message_type, Message.MESSAGE_TYPE_GROUP)

    def test_build_linebot_message(self):
        message = Message.objects.get(pk=self.pk)
        bot_msg = message.build_linebot_message()

        self.assertIsInstance(bot_msg, list)
        self.assertListEqual(
            bot_msg,
            [TextSendMessage("1"), TextSendMessage("2")])


class CircularGroupMessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        message = Message.objects.create(
            message_type=Message.MESSAGE_TYPE_GROUP)
        message.items.add(message)
        cls.pk = message.pk

    def test_build_linebot_message(self):
        message = Message.objects.get(pk=self.pk)
        with self.assertRaises(ValueError):
            message.build_linebot_message()


class GroupInGroupMessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        message = Message.objects.create(
            message_type=Message.MESSAGE_TYPE_GROUP)
        message.items.add(
            Message.objects.create(
                message_type=Message.MESSAGE_TYPE_TEXT, text="1"),
            Message.objects.create(message_type=Message.MESSAGE_TYPE_GROUP))
        cls.pk = message.pk

    def test_build_linebot_message(self):
        message = Message.objects.get(pk=self.pk)
        with self.assertRaises(ValueError):
            message.build_linebot_message()


class TooManyChildGroupMessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        message = Message.objects.create(
            message_type=Message.MESSAGE_TYPE_GROUP)
        message.items.add(*(Message.objects.create(
            message_type=Message.MESSAGE_TYPE_TEXT, text=str(i))
                            for i in range(6)))
        cls.pk = message.pk

    def test_build_linebot_message(self):
        message = Message.objects.get(pk=self.pk)
        with self.assertRaises(ValueError):
            message.build_linebot_message()
