from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from skorunkac.polls import views


admin.site.site_header = 'Skorun Kaç?'
admin.site.site_title = 'Skorun Kaç?'


urlpatterns = [
    path('yonetim/', admin.site.urls),

    path('', views.init_poll, name='init_poll'),
    path('<int:poll_id>/', views.result, name='result'),
    path('<slug:session_slug>/', views.init_poll, name='init_poll'),
    path('<int:poll_id>/<int:page_no>/', views.questions, name='questions'),
    path('<int:poll_id>/kaynak/', views.suggest, name='suggest'),
]
