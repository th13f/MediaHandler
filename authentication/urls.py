from django.conf.urls import patterns, include, url
from django.contrib import admin
from authentication import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^profile/', views.profile_view, name='profile'),
)
