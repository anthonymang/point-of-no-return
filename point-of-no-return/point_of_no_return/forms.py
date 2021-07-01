from django import forms
from django.forms.models import ModelForm
from taggit.managers import TaggableManager
from .models import *

class SearchForm(forms.Form):
    URI = forms.CharField(label='URI', max_length=100)
    search_type = forms.ChoiceField(label = 'Music Type', choices = (
        ('Album', 'Album'),
        ('Track', 'Track'),
    ))

class ArtistCreateForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['location', 'bio', 'bandcamp_link', 'instagram_link', 'discogs_link', 'spotify_embed', 'tags']

