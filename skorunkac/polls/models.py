from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'


class Question(models.Model):
    question = models.CharField(max_length=250)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    order = models.PositiveSmallIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Soru'
        verbose_name_plural = 'Sorular'
        ordering = ('order', 'id')


class Media(models.Model):
    categories = models.ManyToManyField(Category)
    content = models.FileField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.content or self.url

    def clean(self):
        if not [bool(self.content), bool(self.url)].count(True) == 1:
            raise ValidationError('URL ya da icerik alanlari doldurulmali')

    class Meta:
        verbose_name = 'Medya'
        verbose_name_plural = 'Medya'


class Session(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('skorunkac.polls.views.details', args=[str(self.id)])

    class Meta:
        verbose_name = 'Oturum'
        verbose_name_plural = 'Oturumlar'


class Poll(models.Model):
    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        choices=(
            ('m', 'erkek'),
            ('f', 'kadın'),
            ('qm', 'kuir erkek'),
            ('qf', 'kuir kadın'),
        ),
    )
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    education = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        choices=(
            (0, 'yok'),
            (1, 'ilk öğrenim'),
            (2, 'lise'),
            (3, 'üniversite'),
            (4, 'yüksek lisans'),
            (5, 'doktora'),
        ),
    )
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Anket'
        verbose_name_plural = 'Anketler'


class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.SmallIntegerField(
        choices=(
            (0, 'kesinlikle katılmıyorum'),
            (1, 'kısmen katılmıyorum'),
            (2, 'kararsızım'),
            (3, 'kısmen katılıyorum'),
            (4, 'kesinlikle katılıyorum'),
        ),
        default=0,
    )

    class Meta:
        verbose_name = 'Cevap'
        verbose_name_plural = 'Cevaplar'
        unique_together = ('poll', 'question')
