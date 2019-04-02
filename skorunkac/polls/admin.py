import csv
from io import StringIO, BytesIO
from django.http import HttpResponse
from django.contrib import admin
import qrcode
from skorunkac.polls.models import Question, Media, Session, Poll, Category, Answer, QuestionSource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionSource)
class QuestionSourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('poll', 'session', 'question', 'answer',)
    actions = ['download']
    list_filter = ['poll__session', 'poll__gender', 'poll__education', 'poll__lifestyle', 'question']

    def poll(self, answer):
        return answer.poll

    def session(self, answer):
        return answer.poll.session

    def question(self, answer):
        return answer.question

    def download(self, request, qs):
        f = StringIO()
        writer = csv.writer(f)
        for answer in qs:
            writer.writerow([answer.poll.session, answer.poll, answer.question, answer.answer])
        f.seek(0)
        response = HttpResponse(
            f.read(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="cevaplar.csv"'
        return response


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'created', 'active', 'average_score')
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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_f', 'inverse_score', 'category', 'order', 'active', 'source')
    list_editable = ('category', 'order', 'active', 'question_f', 'inverse_score', 'source')


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('session', 'started', 'ended', 'score', 'gender', 'age', 'education', 'lifestyle')
    list_filter = ['session', 'started', 'gender', 'education', 'lifestyle']


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cats', 'description', 'active',)
    list_editable = ('active',)

    def cats(self, media):
        return ', '.join(list(media.categories.values_list('name', flat=True)))
    cats.short_description = 'kategoriler'
