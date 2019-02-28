# Generated by Django 2.1.5 on 2019-02-26 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_question_question_f'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='inverse_score',
            field=models.BooleanField(default=False, verbose_name='ters skor'),
        ),
        migrations.AddField(
            model_name='session',
            name='attendee_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='katılımcı sayısı'),
        ),
        migrations.AddField(
            model_name='session',
            name='institution_type',
            field=models.CharField(blank=True, choices=[('ö', 'özel şirket'), ('s', 'sivil toplum örgütü'), ('k', 'kamu kuruluşu')], max_length=4, null=True, verbose_name='oturum sahibi'),
        ),
        migrations.AddField(
            model_name='session',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='notlar'),
        ),
        migrations.AddField(
            model_name='session',
            name='type',
            field=models.CharField(blank=True, choices=[('p', 'panel'), ('s', 'söyleşi'), ('t', 'tanıtım toplantısı')], max_length=4, null=True, verbose_name='oturum tipi'),
        ),
        migrations.AddField(
            model_name='session',
            name='woman_ratio',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='kadın katılımcı oranı'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='ended',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='bitiş'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='score',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='skor'),
        ),
    ]