# Generated by Django 2.1.5 on 2019-01-17 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20190117_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='questons',
            new_name='question',
        ),
    ]
