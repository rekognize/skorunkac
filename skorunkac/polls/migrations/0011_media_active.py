# Generated by Django 2.1.5 on 2019-01-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20190119_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
