# Generated by Django 4.2.2 on 2023-07-25 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_remove_notification_subcriber_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('TIME_TRACKING_HISTORY', 'TIME_TRACKING_HISTORY'), ('EXPIRED_TASK', 'EXPIRED_TASK'), ('ASSIGN_TASK', 'ASSIGN_TASK')], max_length=128),
        ),
    ]