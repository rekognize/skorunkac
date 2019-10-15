from django.contrib import admin
from django.urls import path
from skorunkac.polls import views
from skorunkac.views import set_language


admin.site.site_header = 'Skorun Kaç?'
admin.site.site_title = 'Skorun Kaç?'


urlpatterns = [
    path('yonetim/', admin.site.urls),
    path('lang/', set_language, name='set_lang'),

    path('', views.init_poll, name='init_poll'),
    path('<int:poll_id>/', views.result, name='result'),
    path('<slug:session_slug>/', views.init_poll, name='init_poll'),
    path('<int:poll_id>/<int:page_no>/', views.questions, name='questions'),
    path('<int:poll_id>/kaynak/', views.suggest, name='suggest'),
]
