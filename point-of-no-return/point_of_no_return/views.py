from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import SearchForm
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
        form = SearchForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data['URI']
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

            if search_type == 'Album':
                headers = {
                    "Authorization": "Bearer " + token,
                }
                album_url = f'https://api.spotify.com/v1/albums/{uri}?market=US'
                res = requests.get(url=album_url, headers=headers)
                album_json = json.dumps(res.json())
                album = json.loads(album_json)
                artist_uri = album['artists'][0]['id']
                pp.pprint(album)
                
                artist, created = Artist.objects.get_or_create(spotify_uri=artist_uri)
                if created == True:
                    artist_url = f'https://api.spotify.com/v1/artists/{artist_uri}?market=US'
                    artist_res = requests.get(url=artist_url, headers=headers)
                    artist_json = json.dumps(artist_res.json())
                    this_artist = json.loads(artist_json)
                    print(this_artist['name'])
                    artist.name = this_artist['name']
                    artist.spotify_link = this_artist['external_urls']['spotify']
                    artist.artist_img = this_artist['images'][0]['url']
                    artist.save()

                    return redirect(f'/artist/create/{artist_uri}')

                
                print(artist, created)
                
                # pp.pprint(album['artists'][0]['href'])

            # elif search_type == 'Artist':
            #     headers = {
            #         "Authorization": "Bearer " + token
            #     }
            #     artist_url = f'https://api.spotify.com/v1/artists/{uri}?market=US'
            #     res = requests.get(url=artist_url, headers=headers)
            #     print(json.dumps(res.json(), indent=2))


            elif search_type == 'Track':
                headers = {
                    "Authorization": "Bearer " + token
                }
                track_url = f'https://api.spotify.com/v1/tracks/{uri}?market=US'
                res = requests.get(url=track_url, headers=headers)
                print(json.dumps(res.json(), indent=2))


            
            return redirect('/add')
    else:
        form = SearchForm()

    return render(request, 'add.html', {'form': form})
