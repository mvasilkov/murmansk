# Generated by Django 2.0.2 on 2018-03-01 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='is_collapsed',
            field=models.BooleanField(default=False),
        ),
    ]
