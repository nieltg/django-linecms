from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, PostbackEvent, TextMessage

from .models import Message, Postback

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

            print("GET EVENT")

            if isinstance(event, MessageEvent):
                print("MESSAGE EVENT")
                if isinstance(event.message, TextMessage):
                    print("TEXT MESSAGE")
                    action = Message.objects.filter(
                        text=event.message.text).first()
            elif isinstance(event, PostbackEvent):
                print("POSTBACK EVENT")
                action = Postback.objects.filter(
                    data=event.postback.data).first()

            if action is not None:
                print("ACTION")
                action.handle_event(event, line_bot_api)

            print("DONE EVENT")

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
