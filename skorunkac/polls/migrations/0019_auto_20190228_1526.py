# Generated by Django 2.1.5 on 2019-02-28 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20190228_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionsource',
            options={'verbose_name': 'kaynak', 'verbose_name_plural': 'kaynaklar'},
        ),
        migrations.RenameField(
            model_name='session',
            old_name='woman_ratio',
            new_name='woman_attendee_count',
        ),
    ]
