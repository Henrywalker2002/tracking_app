# Generated by Django 4.2.2 on 2023-07-04 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0003_rename_subcriber_id_notification_subcriber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='subcriber',
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
