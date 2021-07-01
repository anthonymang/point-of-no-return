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
                    return HttpResponseRedirect('/index')
                else:
                    print('The account has been disabled.')
                    return HttpResponseRedirect('/signup')
        else:
            print('The username and/or password is incorrect.')
            return HttpResponseRedirect('/login')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

# def login_view(request):
#     if request.method is not 'POST':
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})
  
#     form = AuthenticationForm(request, request.POST)
  
#     if not form.is_valid():
#         print('-----------------------The username and/or password was incorrect')
#         return redirect('/index')
    
#     u = form.cleaned_data['username']
#     p = form.cleaned_data['password']
#     user = authenticate(username=u, password=p)

#     if not user.is_active:
#         print('The account has been disabled')
#         return redirect('/index')
    
#     login(request, user)
#     return redirect('/index')

def logout_view(request):
    logout(request)
    return redirect('/login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/index')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def add(request):
    if request.method == 'POST':
        form = ArtistSearchForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data['URI']
            # search_type = form.cleaned_data['search_type']

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
                print('----- ARTIST -----', artist)

                return redirect(f'/artist/create/{uri}')

            else:
                return redirect(f'/artist/new-music/{uri}')

        else:
            print('----Error in artist create----')
            return redirect('/add')  



            # if search_type == 'Album':
            #     headers = {
            #         "Authorization": "Bearer " + token,
            #     }
            #     album_url = f'https://api.spotify.com/v1/albums/{uri}?market=US'
            #     res = requests.get(url=album_url, headers=headers)
            #     album_json = json.dumps(res.json())
            #     album = json.loads(album_json)
            #     artist_uri = album['artists'][0]['id']
            #     pp.pprint(album)
                
            #     artist, created = Artist.objects.get_or_create(spotify_uri=artist_uri)
            #     if created == True:
            #         # artist_url = f'https://api.spotify.com/v1/artists/{artist_uri}?market=US'
            #         # artist_res = requests.get(url=artist_url, headers=headers)
            #         # artist_json = json.dumps(artist_res.json())
            #         # this_artist = json.loads(artist_json)
            #         print(this_artist['name'])
            #         artist.name = this_artist['name']
            #         artist.spotify_link = this_artist['external_urls']['spotify']
            #         artist.artist_img = this_artist['images'][0]['url']
            #         artist.save()

            #         return redirect(f'/artist/create/{artist_uri}')

            #     else:
            #         return redirect(f'/music/create/')    
                                
            #     # pp.pprint(album['artists'][0]['href'])

            # # elif search_type == 'Artist':
            # #     headers = {
            # #         "Authorization": "Bearer " + token
            # #     }
            # #     artist_url = f'https://api.spotify.com/v1/artists/{uri}?market=US'
            # #     res = requests.get(url=artist_url, headers=headers)
            # #     print(json.dumps(res.json(), indent=2))


            # elif search_type == 'Track':
            #     headers = {
            #         "Authorization": "Bearer " + token
            #     }
            #     track_url = f'https://api.spotify.com/v1/tracks/{uri}?market=US'
            #     res = requests.get(url=track_url, headers=headers)
            #     track_json = json.dumps(res.json())
            #     track = json.loads(track_json)
            #     artist_uri = track['artists'][0]['id']
            #     pp.pprint(track)
                
            #     artist, created = Artist.objects.get_or_create(spotify_uri=artist_uri)
            #     if created == True:
            #         artist_url = f'https://api.spotify.com/v1/artists/{artist_uri}?market=US'
            #         artist_res = requests.get(url=artist_url, headers=headers)
            #         artist_json = json.dumps(artist_res.json())
            #         this_artist = json.loads(artist_json)
            #         print(this_artist['name'])
            #         artist.name = this_artist['name']
            #         artist.spotify_link = this_artist['external_urls']['spotify']
            #         artist.artist_img = this_artist['images'][0]['url']
            #         artist.save()

            #         return redirect(f'/artist/create/{artist_uri}')

                
            #     print(artist, created)


            
            # return redirect('/add')
    else:
        form = ArtistSearchForm()

    return render(request, 'add.html', {'form': form})

def artist_create(request, uri):
    artist = get_object_or_404(Artist, spotify_uri=uri)
    print(artist)
    if request.method == 'POST':
        print('in post request')
        form = ArtistCreateForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save(commit=False)
            # print('inside update')
            # artist.location = form.cleaned_data['location']
            # artist.bio = form.cleaned_data['bio']
            # artist.bandcamp_link = form.cleaned_data['bandcamp_link']
            # artist.instagram_link = form.cleaned_data['instagram_link']
            # artist.discogs_link = form.cleaned_data['discogs_link']
            # artist.spotify_embed = form.cleaned_data['spotify_embed']
            # artist.tags = form.cleaned_data['tags']
            # artist.save()
            artist.save()
            form.save_m2m()
            return redirect(f'/artist/new-music/{uri}')
        else:
            print('form not valid')
            print('Errors: ', form.errors, form.non_field_errors)
            return redirect(f'/artist/create/{uri}')

    else:
        print(uri)
        form = ArtistCreateForm()
    return render(request, 'artist_create.html', {'form': form, 'uri':uri})


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
                print('Search Type Album')
                album_url = f'https://api.spotify.com/v1/albums/{form_uri}?market=US'
                res = requests.get(url=album_url, headers=headers)
                album_json = json.dumps(res.json())
                album = json.loads(album_json)
                music = Music.objects.create(spotify_uri=form_uri, name=album['name'],album_art = album['images'][0]['url'], released_by = album['label'], release_date = album['release_date'], user = request.user, curator = Curator.objects.get(user=request.user))
                music.artist.add(Artist.objects.get(spotify_uri=uri))

                # music.name = album['name']
                # music.album_art = album['images'][0]['url']
                # music.released_by = album['label']
                # music.release_date = album['release_date']
                # music.user = request.user
                # music.curator = Curator.objects.get(user=request.user)
                # music.artist.add(Artist.objects.get(spotify_uri=uri))

                return redirect(f'/artist/new-music/{uri}/{form_uri}')

            # if search_type == 'Track':
            #     track_url = f'https://api.spotify.com/v1/tracks/{form_uri}?market=US'
            #     res = requests.get(url=track_url, headers=headers)
            #     track_json = json.dumps(res.json())
            #     track = json.loads(track_json)

            #     music.name = track['name']
            #     music.album_art = track['images'][0]['url']
            #     music.released_by = track['label']
            #     music.release_date = track['release_date']
            #     music.user = request.user
            #     music.curator = Curator.objects.get(user=request.user)
            #     music.save()
            #     music.artist.add(Artist.objects.get(spotify_uri=uri))

            #     return redirect(f'/artist/new-music/{uri}/{form_uri}')

            else:
                return response('<h1>Redirecting to music page</h1>')
    else:
        form = MusicSearchForm()
    
    return render(request, 'music_search.html', {'form': form, 'uri': uri})


def music_create(request, uri, form_uri):
    if request.method == 'POST':
        music = get_object_or_404(Music, spotify_uri=form_uri)

        print('hello')
        form = MusicCreateForm(request.POST, instance=music)
        if form.is_valid():
            music = form.save(commit=False)
            # print('inside update')
            # artist.location = form.cleaned_data['location']
            # artist.bio = form.cleaned_data['bio']
            # artist.bandcamp_link = form.cleaned_data['bandcamp_link']
            # artist.instagram_link = form.cleaned_data['instagram_link']
            # artist.discogs_link = form.cleaned_data['discogs_link']
            # artist.spotify_embed = form.cleaned_data['spotify_embed']
            # artist.tags = form.cleaned_data['tags']
            # artist.save()
            music.save()
            form.save_m2m()
            return redirect('/add')
        else:
            print('form not valid')
            print('Errors: ', form.errors, form.non_field_errors)
            return redirect(f'/artist/new-music/{uri}/{form_uri}')

    
    else:
        print('world')
        form = MusicCreateForm()   
    
    return render(request, 'music_search.html', {'form': form, 'uri': uri, 'form_uri': form_uri})

