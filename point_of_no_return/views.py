from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, response
from .forms import *
import requests
import base64
import json
import pprint
from .models import *
from .filters import *
from django.contrib.auth.decorators import login_required


from decouple import config
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
# Create your views here.

def index(request):
    return render(request, 'index.html')


def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print('The account has been disabled.')
                    return HttpResponseRedirect('/signup')
        else:
            print('The username and/or password is incorrect.')
            return HttpResponseRedirect('/login')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('/login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        return render(request, 'auth/signup.html', {'form': form})

@login_required
def add(request):
    if request.method == 'POST':
        form = ArtistSearchForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data['URI']

            url = 'https://accounts.spotify.com/api/token'
            headers = {}
            data = {}

            message = f"{CLIENT_ID}:{CLIENT_SECRET}"
            messageBytes = message.encode('ascii')
            base64Bytes = base64.b64encode(messageBytes)
            base64Message = base64Bytes.decode('ascii')

            headers['Authorization'] = f'Basic {base64Message}'
            data['grant_type'] = 'client_credentials'

            r = requests.post(url, headers = headers, data=data)

            token = r.json()['access_token']
            pp = pprint.PrettyPrinter(indent=2)
            headers = {
                     "Authorization": "Bearer " + token,
               }
            artist_url = f'https://api.spotify.com/v1/artists/{uri}?market=US'
            artist_res = requests.get(url=artist_url, headers=headers)
            artist_json = json.dumps(artist_res.json())
            this_artist = json.loads(artist_json)
            pp.pprint(this_artist)

            artist, created = Artist.objects.get_or_create(spotify_uri=uri)
            if created == True:
                artist.name = this_artist['name']
                artist.spotify_link = this_artist['external_urls']['spotify']
                artist.artist_img = this_artist['images'][0]['url']
                artist.save()

                return redirect(f'/database/artist/create/{uri}')

            else:
                return redirect(f'/database/music/{uri}')

        else:
            print('----Error in artist create----')
            return redirect('/add')  

    else:
        form = ArtistSearchForm()

    return render(request, 'database/add.html', {'form': form})

@login_required
def artist_create(request, uri):
    artist = get_object_or_404(Artist, spotify_uri=uri)
    if request.method == 'POST':
        print('in post request')
        form = ArtistCreateForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save(commit=False)

            artist.save()
            form.save_m2m()
            return redirect(f'/database/music/{uri}')
        else:
            print('form not valid')
            print('Errors: ', form.errors, form.non_field_errors)
            return redirect(f'/database/artist/create/{uri}')

    else:
        form = ArtistCreateForm()
    return render(request, 'database/artist_create.html', {'form': form, 'uri':uri})


@login_required
def music_add(request, uri):
    if request.method == 'POST':
        form = MusicSearchForm(request.POST)
        if form.is_valid():
            form_uri = form.cleaned_data['URI']
            search_type = form.cleaned_data['search_type']

            url = 'https://accounts.spotify.com/api/token'
            headers = {}
            data = {}

            message = f"{CLIENT_ID}:{CLIENT_SECRET}"
            messageBytes = message.encode('ascii')
            base64Bytes = base64.b64encode(messageBytes)
            base64Message = base64Bytes.decode('ascii')

            headers['Authorization'] = f'Basic {base64Message}'
            data['grant_type'] = 'client_credentials'

            r = requests.post(url, headers = headers, data=data)

            token = r.json()['access_token']
            pp = pprint.PrettyPrinter(indent=2)
            headers = {
                     "Authorization": "Bearer " + token,
               }

            print('form valid')


            if search_type == 'Album':
                album_url = f'https://api.spotify.com/v1/albums/{form_uri}?market=US'
                res = requests.get(url=album_url, headers=headers)
                album_json = json.dumps(res.json())
                album = json.loads(album_json)
                music = Music.objects.create(spotify_uri=form_uri, name=album['name'],album_art = album['images'][0]['url'], released_by = album['label'], release_date = album['release_date'], user = request.user, curator = Curator.objects.get(user=request.user))
                music.artist.add(Artist.objects.get(spotify_uri=uri))

 
                return redirect(f'/database/music/finish/{form_uri}')

            if search_type == 'Track':
                track_url = f'https://api.spotify.com/v1/tracks/{form_uri}?market=US'
                res = requests.get(url=track_url, headers=headers)
                track_json = json.dumps(res.json())
                track = json.loads(track_json)

                music = Music.objects.create(spotify_uri=form_uri, name=track['name'],album_art = track['images'][0]['url'], released_by = track['label'], release_date = track['release_date'], user = request.user, curator = Curator.objects.get(user=request.user))
                music.artist.add(Artist.objects.get(spotify_uri=uri))

                return redirect(f'/database/music/finish/{form_uri}')

            else:
                return response('<h1>Redirecting to music page</h1>')
    else:
        form = MusicSearchForm()
    
    return render(request, 'database/music_search.html', {'form': form, 'uri': uri})

@login_required
def music_create(request, form_uri):
    print('in music create route')
    if request.method == 'POST':
        print('in post request')
        music = get_object_or_404(Music, spotify_uri=form_uri)

        
        form = MusicCreateForm(request.POST, instance=music)
        if form.is_valid():
            music = form.save(commit=False)

            music.save()
            form.save_m2m()
            return redirect(f'/music/{form_uri}')
        else:
            print('form not valid')
            print('Errors: ', form.errors, form.non_field_errors)
            return redirect(f'/database/music/finish/{form_uri}')

    
    else:
        form = MusicCreateForm()   
    
    return render(request, 'database/music_create.html', {'form': form, 'form_uri': form_uri})

def music_show(request, uri):
    music = get_object_or_404(Music, spotify_uri=uri)


    return render(request, 'show/music_show.html', {'music': music})


def artist_show(request, uri):
    artist = get_object_or_404(Artist, spotify_uri=uri)
    music = Music.objects.filter(artist=artist)

    return render(request, 'show/artist_show.html', {'artist': artist, 'music': music})

def search_music(request):
    music = Music.objects.all()
    music_filter = MusicFilter(request.GET, queryset=music)
    music = music_filter.qs
    return render(request, 'search/music.html', {'filter': music_filter, 'music': music})

def tag_show(request, slug):
    music = Music.objects.filter(tags__name__in=[slug])
    artists = Artist.objects.filter(tags__name__in=[slug])

    return render(request, 'show/tag_show.html', {'slug': slug, 'music': music, 'artists': artists})