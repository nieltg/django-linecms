from django.urls import path

from .views import WebhookView

urlpatterns = [
    path('callback/', WebhookView.as_view()),
]
