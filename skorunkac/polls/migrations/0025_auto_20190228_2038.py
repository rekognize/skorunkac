# Generated by Django 2.1.5 on 2019-02-28 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_auto_20190228_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='employee_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='kurum çalışan sayısı'),
        ),
        migrations.AlterField(
            model_name='session',
            name='name',
            field=models.CharField(max_length=100, verbose_name='oturum adı'),
        ),
        migrations.AlterField(
            model_name='session',
            name='woman_employee_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='kurum kadın çalışan sayısı'),
        ),
    ]
