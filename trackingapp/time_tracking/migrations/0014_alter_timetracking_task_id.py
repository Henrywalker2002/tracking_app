# Generated by Django 4.2.2 on 2023-07-25 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracking', '0013_remove_workflow_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetracking',
            name='task_id',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]