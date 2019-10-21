import csv
from io import StringIO, BytesIO
from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin
from django.db.models import Sum, Count, Avg, F, Q
import qrcode
from skorunkac.polls.models import Question, Media, Session, Poll, Category, Answer, QuestionSource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'average_score']

    def average_score(self, category):
        score = category.question_set.filter(active=True).filter(
            inverse_score=False
        ).aggregate(total_points=Sum('answer__answer'))['total_points'] or 0
        inverse_score = category.question_set.filter(active=True).filter(
            inverse_score=True
        ).aggregate(total_points=Sum('answer__answer'))['total_points'] or 0
        answer_count = Answer.objects.filter(question__category=category).filter(question__active=True).count()
        inverse_answer_count = Answer.objects.filter(question__category=category).filter(question__active=True).filter(question__inverse_score=True).count()
        print(score, inverse_score, answer_count, inverse_answer_count)
        return round(
            100 * (score + (settings.POLL_SETTINGS['ANSWER_STEPS'] * inverse_answer_count - inverse_score)) /
            answer_count / settings.POLL_SETTINGS['ANSWER_STEPS'], 2
        )
    average_score.short_description = 'ortalama'


@admin.register(QuestionSource)
class QuestionSourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('poll', 'session', 'question', 'answer',)
    actions = ['download']
    list_filter = [
        'poll__session',
        'poll__gender',
        'poll__education',
        #'poll__lifestyle',
        'question'
    ]

    def poll(self, answer):
        return answer.poll

    def session(self, answer):
        return answer.poll.session

    def question(self, answer):
        return answer.question

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow([
            'Oturum adı',
            'Anket Id',
            'Soru',
            'Cevap',
            'Cinsiyet',
            'Eğitim durumu',
            'Yaş',
        ])
        for answer in qs:
            writer.writerow([
                answer.poll.session.name,
                answer.poll.id,
                answer.question.question,
                answer.answer,
                answer.poll.get_gender_display(),
                answer.poll.get_education_display(),
                answer.poll.age,
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="cevaplar.csv"'
        return response
    download.short_description = "Cevapları indir"


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name', 'created', 'active', 'participant_count', 'average_score', 'participant_count_m', 'average_score_m',
        'participant_count_f', 'average_score_f'
    )
    list_editable = ('active',)
    actions = ['download_qr_code']

    def download_qr_code(self, request, queryset):
        for session in queryset:
            qr = qrcode.make(f'http://skorunkac.yanindayiz.org{session.get_absolute_url()}')
            with BytesIO() as f:
                qr.save(f, 'PNG')
                f.seek(0)
                response = HttpResponse(
                    f.read(),
                    content_type='image/png'
                )
                response['Content-Disposition'] = f'attachment; filename="{session.slug}.png"'
            return response
    download_qr_code.short_description = "QR kodunu indir"

    def average_score(self, obj):
        return round(obj.poll_set.exclude(score__isnull=True).aggregate(Avg('score'))['score__avg'] or 0, 2)
    average_score.short_description = 'ortalama skor'

    def average_score_m(self, obj):
        return round(obj.poll_set.filter(gender='m').exclude(score__isnull=True).aggregate(Avg('score'))['score__avg'] or 0, 2)
    average_score_m.short_description = 'ortalama skor (erkek)'

    def average_score_f(self, obj):
        return round(obj.poll_set.filter(gender='f').exclude(score__isnull=True).aggregate(Avg('score'))['score__avg'] or 0, 2)
    average_score_f.short_description = 'ortalama skor (kadın)'

    def participant_count(self, obj):
        return round(obj.poll_set.exclude(score__isnull=True).count())
    participant_count.short_description = 'toplam katılımcı'

    def participant_count_m(self, obj):
        return round(obj.poll_set.filter(gender='m').exclude(score__isnull=True).count())
    participant_count_m.short_description = 'toplam katılımcı (erkek)'

    def participant_count_f(self, obj):
        return round(obj.poll_set.filter(gender='f').exclude(score__isnull=True).count())
    participant_count_f.short_description = 'toplam katılımcı (kadın)'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_f', 'question_en', 'question_f_en', 'inverse_score', 'category', 'order', 'active')
    list_editable = ('category', 'order', 'active', 'question_f', 'question_en', 'question_f_en', 'inverse_score')


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = [
        'session',
        'started',
        'ended',
        'score',
        'gender',
        'age',
        'education',
        #'lifestyle'
    ]
    list_filter = [
        'session',
        'started',
        'gender',
        'education',
        #'lifestyle'
    ]
    actions = ['download']

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for poll in qs:
            writer.writerow([
                poll.session,
                poll.get_gender_display(),
                poll.age,
                poll.get_marital_status_display(),
                poll.get_hometown_size_display(),
                poll.score,
            ])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="anketler.csv"'
        return response
    download.short_description = "Anket sonuçlarını indir"


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cats', 'description', 'added', 'active',)
    list_editable = ('active',)

    def cats(self, media):
        return ', '.join(list(media.categories.values_list('name', flat=True)))
    cats.short_description = 'kategoriler'
