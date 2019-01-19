from django.contrib import admin
from django.urls import path
from skorunkac.polls import views


admin.site.site_header = 'Skorun Kaç?'
admin.site.site_title = 'Skorun Kaç?'


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.select_session, name='select_session'),
    path('<int:poll_id>/', views.result, name='result'),
    path('<slug:session_slug>/', views.init_poll, name='init_poll'),
    path('<int:poll_id>/<int:page_no>/', views.questions, name='questions'),
]
