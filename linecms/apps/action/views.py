from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, PostbackEvent, TextMessage

from .models import Message, Postback, InvalidMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            action = None

            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    action = Message.objects.filter(
                        text__iexact=event.message.text).first()
                    if action is None:
                        action = InvalidMessage.objects.order_by('?').first()
            elif isinstance(event, PostbackEvent):
                action = Postback.objects.filter(
                    data=event.postback.data).first()

            if action is not None:
                action.handle_event(event, line_bot_api)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
