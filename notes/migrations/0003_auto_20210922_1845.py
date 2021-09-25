# Generated by Django 3.2.7 on 2021-09-22 13:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_auto_20210922_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='', max_length=10)),
                ('color', models.CharField(default='yellow', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='notesmodel',
            name='contributers',
        ),
        migrations.RemoveField(
            model_name='notesmodel',
            name='labels',
        ),
        migrations.AddField(
            model_name='notesmodel',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notesmodel',
            name='label',
            field=models.ManyToManyField(related_name='labels', to='notes.Labels'),
        ),
    ]