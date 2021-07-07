import django_filters
from django_filters import DateFilter
from django_filters.filters import ChoiceFilter, LookupChoiceFilter, AllValuesFilter, DateFilter, DateFromToRangeFilter, CharFilter, ModelChoiceFilter, DurationFilter, MultipleChoiceFilter
from .models import *
from taggit.managers import TaggableManager

artist_list = []
for artist in Artist.objects.all():
    artist_list.append((artist.id, artist.name))

# for tag in Tag.objects.all()

tag_list = []
label_list = []

for music in Music.objects.all():
    for tag in music.tags.all():
        if tag not in tag_list:
            tag_list.append((tag.id, tag.name))

    if music.released_by not in label_list:
        label_list.append((music.released_by, music.released_by))




# for music in Music.objects.all():
#     label_list.append(music.released_by)

class MusicFilter(django_filters.FilterSet):
    description = CharFilter(field_name = 'description', label='Description',lookup_expr='icontains')
    artist = MultipleChoiceFilter(field_name='artist', choices = artist_list, label= 'artist')
    release_date = DateFromToRangeFilter(field_name = 'release_date')
    tags = MultipleChoiceFilter(field_name = 'tags', choices = tag_list)
    released_by = ChoiceFilter(field_name = 'released_by', choices = label_list)


    class Meta:
        model = Music
        fields = ['curator']