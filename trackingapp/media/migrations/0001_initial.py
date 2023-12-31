# Generated by Django 4.2.2 on 2023-07-03 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('media_from', models.JSONField(db_column='from')),
                ('to', models.JSONField()),
                ('content', models.TextField()),
                ('context_type', models.CharField(choices=[('TEXT_PLAIN', 'TEXT_PLAIN'), ('HTML', 'HTML')], default='TEXT_PLAIN', max_length=128)),
                ('sending_method', models.CharField(choices=[('EMAIL', 'EMAIL'), ('MESSAGE', 'MESSAGE'), ('SMS', 'SMS')], max_length=128)),
                ('status', models.CharField(choices=[('IN_QUEUE', 'IN_QUEUE'), ('IN_PROCESS', 'IN_PROCESS'), ('SUCCESS', 'SUCCESS'), ('FAIL', 'FAIL')], default='IN_QUEUE', max_length=128)),
                ('retry_count', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
