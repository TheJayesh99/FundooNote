# Generated by Django 3.2.7 on 2021-10-18 10:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0003_auto_20210922_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='notesmodel',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notesmodel',
            name='is_binned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notesmodel',
            name='collaborators',
            field=models.ManyToManyField(default=0, related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notesmodel',
            name='label',
            field=models.ManyToManyField(default=0, related_name='labels', to='notes.Labels'),
        ),
    ]