from django.contrib import admin
from skorunkac.polls.models import Question, Media, Session, Poll, Category, Answer



@admin.register(Category, Answer)
class GenericAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'created', 'active',)
    list_editable = ('active',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'active',)
    list_editable = ('category', 'order', 'active',)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('session', 'started', 'ended', 'score', 'gender', 'age', 'education')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cats', 'active',)
    list_editable = ('active',)

    def cats(self, obj):
        return ', '.join(list(obj.categories.values_list('name', flat=True)))
