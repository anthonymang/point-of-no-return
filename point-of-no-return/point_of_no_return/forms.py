from django import forms
from django.forms.models import ModelForm
from taggit.managers import TaggableManager
from .models import *

class ArtistSearchForm(forms.Form):
    URI = forms.CharField(label='Artist URI', max_length=100)

class MusicSearchForm(forms.Form):
    URI = forms.CharField(label='Music URI', max_length=100)
    search_type = forms.ChoiceField(label = 'Music Type', choices = (
        ('Album', 'Album'),
        ('Track', 'Track')
    ))


class ArtistCreateForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['location', 'bio', 'bandcamp_link', 'instagram_link', 'discogs_link', 'spotify_embed', 'tags']

class MusicCreateForm(ModelForm):
    class Meta:
        model = Music
        fields = ['description', 'spotify_embed', 'bandcamp_embed', 'discogs_link', 'release_type', 'curator', 'artist', 'tags']