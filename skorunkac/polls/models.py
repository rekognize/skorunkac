from urllib.parse import urlparse, parse_qs
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField('kategori adı', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'kategori'
        verbose_name_plural = 'kategoriler'


class Question(models.Model):
    question = models.CharField('soru', max_length=250)
    question_f = models.CharField('soru (kadın versiyonu)', blank=True, null=True, max_length=250)
    category = models.ForeignKey(Category, verbose_name='kategori', blank=True, null=True, on_delete=models.SET_NULL)
    order = models.PositiveSmallIntegerField('sıralama', blank=True, null=True)
    inverse_score = models.BooleanField('ters skor', default=False)
    active = models.BooleanField('yayında', default=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'soru'
        verbose_name_plural = 'sorular'
        ordering = ('order', 'id')


class Media(models.Model):
    categories = models.ManyToManyField(Category, verbose_name='kategoriler')
    content = models.FileField('içerik', blank=True, null=True)
    url = models.URLField('bağlantı', blank=True, null=True)
    description = models.TextField('tanım', blank=True, null=True)
    active = models.BooleanField('yayında', default=True)

    def __str__(self):
        return self.content or self.url

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
    name = models.CharField('oturum', max_length=100)
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
    attendee_count = models.PositiveIntegerField('katılımcı sayısı', blank=True, null=True)
    woman_ratio = models.PositiveSmallIntegerField('kadın katılımcı oranı', blank=True, null=True)
    notes = models.TextField('notlar', blank=True, null=True)
    created = models.DateTimeField('eklenme tarihi', auto_now_add=True)
    active = models.BooleanField('yayında', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skorunkac.polls.views.details', args=[str(self.id)])

    class Meta:
        verbose_name = 'oturum'
        verbose_name_plural = 'oturumlar'


class Poll(models.Model):
    session = models.ForeignKey(Session, verbose_name='oturum', blank=True, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(
        'cinsiyet',
        max_length=1, blank=True, null=True,
        choices=(
            ('m', 'erkek'),
            ('f', 'kadın'),
            ('g', 'LGBTI erkek'),
            ('l', 'LGBTI kadın'),
        ),
    )
    age = models.PositiveSmallIntegerField('yaş', blank=True, null=True)
    education = models.PositiveSmallIntegerField(
        'eğitim durumu',
        blank=True, null=True,
        choices=(
            (0, 'Diplomasız okur'),
            (1, 'İlkokul mezunu'),
            (2, 'İlköğretim / Ortaokul mezunu'),
            (3, 'Lise mezunu'),
            (4, 'Yüksekokul mezunu'),
            (5, 'Lisans mezunu'),
            (6, 'Yüksek lisans'),
            (7, 'Doktora'),
        ),
    )
    marital_status = models.CharField(
        'medeni durum',
        max_length=1, blank=True, null=True,
        choices=(
            ('b', 'Bekar'),
            ('s', 'Sözlü / Nişanlı'),
            ('e', 'Evli'),
            ('d', 'Dul'),
            ('a', 'Boşanmış'),
        ),
    )
    hometown_size = models.CharField(
        'büyüdüğünüz yer',
        max_length=1, blank=True, null=True,
        choices=(
            ('k', 'Köy'),
            ('i', 'Kasaba / İlçe'),
            ('s', 'Şehir'),
            ('m', 'Büyükşehir / Metropol'),
        ),
    )
    lifestyle = models.CharField(
        'hayat tarzı',
        max_length=1,
        blank=True,
        null=True,
        choices=(
            ('m', 'modern'),
            ('g', 'geleneksel muhafazakar'),
            ('d', 'dindar muhafazakar'),
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
