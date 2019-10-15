# Generated by Django 2.1.5 on 2019-10-14 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0029_media_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_en',
            field=models.CharField(default='-', max_length=250, verbose_name='soru [EN]'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_f_en',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='soru (kadın versiyonu) [EN]'),
        ),
        migrations.AlterField(
            model_name='media',
            name='added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='eklenme tarihi'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='age',
            field=models.PositiveSmallIntegerField(verbose_name='Your age'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='education',
            field=models.PositiveSmallIntegerField(choices=[(0, 'No formal education'), (1, 'Primary School'), (2, 'Secondary School'), (3, 'High School'), (4, 'College'), (5, 'University'), (6, 'Masters'), (7, 'Doctorate / PhD')], help_text='Final degree', verbose_name='Education'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='hometown_size',
            field=models.CharField(choices=[('k', 'Village'), ('i', 'Town'), ('s', 'City'), ('m', 'Metropolis')], max_length=1, verbose_name='Where You Grew Up'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='lifestyle',
            field=models.CharField(blank=True, choices=[('m', 'Modern'), ('g', 'Conservative'), ('d', 'Religious conservative')], max_length=1, null=True, verbose_name='Life style'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='marital_status',
            field=models.CharField(choices=[('b', 'Single / Not Married'), ('s', 'Has a partner / Engaged'), ('e', 'Married'), ('d', 'Widowed'), ('a', 'Divorced')], max_length=1, verbose_name='Marital Status'),
        ),
    ]