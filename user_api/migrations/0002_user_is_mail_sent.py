# Generated by Django 3.2.7 on 2021-11-03 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_mail_sent',
            field=models.BooleanField(default=False),
        ),
    ]
