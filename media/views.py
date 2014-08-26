from django.http import HttpResponse
from django.shortcuts import render
from media.models import Tag, Song


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
    return render(request, 'media/index.html', {
        'tags': Tag.objects.all()[:20],
        'song_list': get_song_list(8, '')
    })


def suggest_song_view(request):
        starts_with = ''
        if request.method == 'GET':
            starts_with = request.GET['suggestion']

        song_list = get_song_list(8, starts_with)

        return render(request, 'media/song_list.html', {'song_list': song_list })