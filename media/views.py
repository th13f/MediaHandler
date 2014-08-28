from django.core.urlresolvers import reverse
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from tagging.utils import LOGARITHMIC
from tagging.models import Tag, TagManager
from media.forms import TagsForm
from media.models import Song, Artist


def processor(request):
    return {
        'cloud': Tag.objects.cloud_for_model(Song, steps=8, distribution=LOGARITHMIC),
    }


def like_tag_view(request):
    tag_id = None
    if request.method == 'GET':
        tag_id = int(request.GET['tag_id'])

    likes = 0
    if tag_id:
        tag = Tag.objects.get(id=tag_id)
        if tag:
            likes = tag.popularity + 1
            tag.popularity = likes
            tag.save()

    return HttpResponse(likes)


def get_song_list(max_results=0, starts_with=''):
    if starts_with:
        song_list = Song.objects.filter(name__icontains=starts_with)
    else:
        song_list = Song.objects.all()

    if max_results > 0:
        if len(song_list) > max_results:
            song_list = song_list[:max_results]

    #for cat in song_list:
    #        cat.url = encode_url(cat.name)

    return song_list


def index_view(request):
    return render(
        request, 'media/index.html',
        {
            'tags': Tag.objects.all()[:20],
            'song_list': get_song_list(8, ''),
            'tags_form': TagsForm(),
            'artists': Artist.objects.all()[:30],
        },
        context_instance=RequestContext(request, processors=[processor])
    )


def albums_by_artist(request):
    albums = {}
    artist_id = request.GET['artist']
    for album in Artist.objects.get(pk=artist_id).album_set.all():
        albums[album.id]=album.name

    return HttpResponse(json.dumps(albums), content_type="application/json")


def upload(request):
    return HttpResponseRedirect(reverse('media:index'))


def suggest_song_view(request):
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    song_list = get_song_list(8, starts_with)

    return render(request, 'media/song_list.html', {'song_list': song_list})