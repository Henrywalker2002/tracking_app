# Generated by Django 4.2.2 on 2023-07-04 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracking', '0007_timetracking_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetracking',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='timetracking',
            name='note',
            field=models.TextField(null=True),
        ),
    ]
