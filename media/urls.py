from django.conf.urls import patterns, url, include
from django.contrib import admin
from media import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index_view, name='index'),
                       url(r'^like_tag/', views.like_tag_view, name='like_tag'),
                       url(r'^suggest_song/$', views.suggest_song_view, name='suggest_song'),
                       #url(r'^suggest_tag/', views.suggest_tag_view, name='suggest_tag'),
                       #url(r'^register/$', views.register_view, name='register'),
                       #url(r'^logout/$', views.logout_view, name='logout'),
                       #url(r'^profile/$', views.profile_view, name='profile'),
                       )
