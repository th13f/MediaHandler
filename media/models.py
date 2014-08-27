# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
import tagging


class Artist(models.Model):
    name = models.CharField(max_length=100)
    link_to_wiki = models.CharField(max_length=255)
    popularity = models.IntegerField(default='1')

    def __unicode__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=100)
    link_to_wiki = models.CharField(max_length=255)
    popularity = models.IntegerField(default='1')
    artist = models.ForeignKey(Artist)

    def __unicode__(self):
        return self.name


#рудимент для работы облака тегов и лайков
class Tag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    popularity = models.IntegerField(default=1)
    #songs = models.ManyToManyRel(Song)   #обращаться как tag.song_set.all()
    #playlists = models.ManyToManyRel(Playlist)

    def __unicode__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='audio/', null=True)
    user = models.ForeignKey(User)
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)

    def __unicode__(self):
        return self.name

tagging.register(Song)


class Playlist(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)#, through='Playlist_songs')

    def __unicode__(self):
        return self.name


#так себе идея
"""
class Playlist_songs(models.Model):
    playlist = models.ForeignKey(Playlist)
    song = models.ForeignKey(Song)
    order = models.IntegerField(default=0,required=False)
"""