# Generated by Django 2.1.5 on 2019-01-16 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_session_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Cevap', 'verbose_name_plural': 'Cevaplar'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategori', 'verbose_name_plural': 'Kategoriler'},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name': 'Medya', 'verbose_name_plural': 'Medya'},
        ),
        migrations.AlterModelOptions(
            name='poll',
            options={'verbose_name': 'Anket', 'verbose_name_plural': 'Anketler'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Soru', 'verbose_name_plural': 'Sorular'},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'verbose_name': 'Oturum', 'verbose_name_plural': 'Oturumlar'},
        ),
        migrations.AddField(
            model_name='session',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
