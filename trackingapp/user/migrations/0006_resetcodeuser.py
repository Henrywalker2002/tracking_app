# Generated by Django 4.2.2 on 2023-07-14 04:56

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_rename_create_at_user_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetCodeUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('code', models.CharField(max_length=6)),
                ('expired_time', models.DateTimeField(default=datetime.datetime(2023, 7, 14, 5, 1, 37, 175139, tzinfo=datetime.timezone.utc))),
            ],
        ),
    ]