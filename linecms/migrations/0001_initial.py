# Generated by Django 2.0.3 on 2018-06-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('message_type',
                 models.IntegerField(
                     choices=[(0, 'Message Group'), (1, 'Text Message')],
                     verbose_name='Message type')),
                ('text', models.TextField(
                    max_length=2000, verbose_name='Text')),
                ('items',
                 models.ManyToManyField(
                     related_name='_message_items_+',
                     to='linecms.Message',
                     verbose_name='Group Items')),
            ],
        ),
    ]
