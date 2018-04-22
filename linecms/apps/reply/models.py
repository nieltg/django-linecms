from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from linebot.models import ImageSendMessage, TextSendMessage


class Text(models.Model):
    """LINE text message model."""

    text = models.TextField(_('Text'), max_length=2000)

    def get_line_bot_object(self):
        return TextSendMessage(text=self.text)

    def __str__(self):
        return self.text[:100]


class Image(models.Model):
    """LINE image message model."""

    image = ProcessedImageField(
        upload_to='images',
        processors=[ResizeToFill(1024, 1024)],
        format='JPEG',
        options={'quality': 60})

    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(240, 240)],
        format='JPEG',
        options={'quality': 60})

    def get_line_bot_object(self):
        return ImageSendMessage(
            original_content_url=self.image,
            preview_image_url=self.image_thumbnail)


class Group(models.Model):
    """Group action."""

    def get_line_bot_object(self):
        bot_obj = []
        for item in self.group_item_set.all():
            bot_obj.append(item.get_line_bot_object())
        return bot_obj


class AbstractAction(models.Model):
    """Reply action."""

    class Meta:
        abstract = True

    REPLY_TEXT = 1
    REPLY_GROUP = 2
    REPLY_IMAGE = 3
    REPLY_CHOICES = (
        (REPLY_TEXT, _("Text")),
        (REPLY_GROUP, _("Group")),
        (REPLY_IMAGE, _("Image")),
    )

    reply = models.IntegerField(choices=REPLY_CHOICES)
    reply_text = models.ForeignKey(
        Text, on_delete=models.PROTECT, null=True, blank=True)
    reply_group = models.ForeignKey(
        Group, on_delete=models.PROTECT, null=True, blank=True)
    reply_image = models.ForeignKey(
        Image, on_delete=models.PROTECT, null=True, blank=True)

    def get_line_bot_object(self):
        providers = {
            self.REPLY_TEXT: self.reply_text,
            self.REPLY_GROUP: self.reply_group,
            self.REPLY_IMAGE: self.reply_image,
        }

        provider = providers[self.reply]
        return provider.get_line_bot_object()


class GroupItem(AbstractAction):
    """Group action item."""

    parent = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='group_item_set')
    reply_group = None

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        if 'reply' not in exclude and self.reply == self.REPLY_GROUP:
            raise ValidationError({
                AbstractAction.reply:
                _("Unable to add group in group")
            })
