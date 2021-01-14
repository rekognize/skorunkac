from urllib.parse import urlparse, parse_qs
from django.db import models
from django.urls import reverse
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from skorunkac.cities.models import City


class Category(models.Model):
    name = models.CharField('kategori adı', max_length=100)
    description = models.CharField('açıklama', max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'kategori'
        verbose_name_plural = 'kategoriler'


class QuestionSource(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'kaynak'
        verbose_name_plural = 'kaynaklar'


class Question(models.Model):
    question = models.CharField('soru', max_length=250)
    question_en = models.CharField('soru [EN]', max_length=250)
    question_f = models.CharField('soru (kadın versiyonu)', blank=True, null=True, max_length=250)
    question_f_en = models.CharField('soru (kadın versiyonu) [EN]', blank=True, null=True, max_length=250)
    category = models.ForeignKey(Category, verbose_name='kategori', blank=True, null=True, on_delete=models.SET_NULL)
    order = models.PositiveSmallIntegerField('sıralama', blank=True, null=True)
    inverse_score = models.BooleanField('ters skor', default=False)
    source = models.ForeignKey(QuestionSource, verbose_name='kaynak', blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField('yayında', default=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'soru'
        verbose_name_plural = 'sorular'
        ordering = ('order', 'id')


class Media(models.Model):
    categories = models.ManyToManyField(Category, verbose_name='kategoriler')
    url = models.URLField('bağlantı')
    description = models.TextField('tanım', blank=True, null=True)
    active = models.BooleanField('yayında', default=True)
    added = models.DateTimeField('eklenme tarihi', auto_now_add=True)

    def __str__(self):
        return self.url

    def clean(self):
        if not [bool(self.content), bool(self.url)].count(True) == 1:
            raise ValidationError('URL ya da icerik alanlari doldurulmali')
        if self.url and 'youtube.com' in self.url and 'watch?v=' in self.url:
            parts = urlparse(self.url)
            params = parse_qs(parts.query)
            v = params.get('v')
            if v:
                self.url = f"https://youtube.com/embed/{v[0]}"
            else:
                raise ValidationError('Youtube adresi geçersiz')

    class Meta:
        verbose_name = 'medya'
        verbose_name_plural = 'medya'


class Session(models.Model):
    name = models.CharField('oturum adı', max_length=100)
    slug = models.SlugField('bağlantı adı')
    type = models.CharField(
        'oturum tipi',
        max_length=4,
        blank=True, null=True,
        choices=(
            ('p', 'panel'),
            ('s', 'söyleşi'),
            ('t', 'tanıtım toplantısı'),
        )
    )
    institution_type = models.CharField(
        'oturum sahibi',
        max_length=4,
        blank=True, null=True,
        choices=(
            ('ö', 'özel şirket'),
            ('s', 'sivil toplum örgütü'),
            ('k', 'kamu kuruluşu'),
        )
    )
    employee_count = models.PositiveIntegerField('kurum çalışan sayısı', blank=True, null=True)
    woman_employee_count = models.PositiveIntegerField('kurum kadın çalışan sayısı', blank=True, null=True)
    attendee_count = models.PositiveIntegerField('etkinlik katılımcı sayısı', blank=True, null=True)
    woman_attendee_count = models.PositiveIntegerField('etkinlik kadın katılımcı sayısı', blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='il', blank=True, null=True, on_delete=models.SET_NULL)
    location = models.CharField('yer', max_length=200, blank=True, null=True)
    notes = models.TextField('notlar', blank=True, null=True)
    created = models.DateTimeField('eklenme tarihi', auto_now_add=True)
    active = models.BooleanField('yayında', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('init_poll', kwargs={'session_slug': self.slug})

    class Meta:
        verbose_name = 'oturum'
        verbose_name_plural = 'oturumlar'


class Poll(models.Model):
    session = models.ForeignKey(Session, verbose_name='oturum', blank=True, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        choices=(
            ('m', _('Male')),
            ('f', _('Female')),
        ),
    )
    age = models.PositiveSmallIntegerField(_('Your age'))
    education = models.PositiveSmallIntegerField(
        _('Education'),
        help_text=_('Final degree'),
        choices=(
            (0, _('No formal education')),
            (1, _('Primary School')),
            (2, _('Secondary School')),
            (3, _('High School')),
            (4, _('College')),
            (5, _('University')),
            (6, _('Masters')),
            (7, _('Doctorate / PhD')),
            (8, _('Student')),
        ),
    )
    marital_status = models.CharField(
        _('Marital Status'),
        max_length=1,
        choices=(
            ('b', _('Single / Not Married')),
            ('s', _('Has a partner / Engaged')),
            ('e', _('Married')),
            ('d', _('Widowed')),
            ('a', _('Divorced')),
        ),
    )
    hometown_size = models.CharField(
        _('Where You Grew Up'),
        max_length=1,
        choices=(
            ('k', _('Village')),
            ('i', _('Town')),
            ('s', _('City')),
            ('m', _('Metropolis')),
        ),
    )
    lifestyle = models.CharField(
        _('Life style'),
        max_length=1, blank=True, null=True,
        choices=(
            ('m', _('Modern')),
            ('g', _('Conservative')),
            ('d', _('Religious conservative')),
        ),
    )
    started = models.DateTimeField('başlangıç', auto_now_add=True, editable=False)
    ended = models.DateTimeField('bitiş', blank=True, null=True, editable=False)
    score = models.FloatField('skor', blank=True, null=True, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'anket'
        verbose_name_plural = 'anketler'


class Answer(models.Model):
    poll = models.ForeignKey(Poll, verbose_name='anket', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='soru', on_delete=models.CASCADE)
    answer = models.PositiveSmallIntegerField('cevap', default=0)

    class Meta:
        verbose_name = 'cevap'
        verbose_name_plural = 'cevaplar'
        unique_together = ('poll', 'question')
