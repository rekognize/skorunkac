# Generated by Django 2.1.5 on 2019-01-19 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20190119_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='content',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
