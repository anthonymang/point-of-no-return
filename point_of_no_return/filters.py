import django_filters
from django_filters import DateFilter
from django_filters.filters import ChoiceFilter, LookupChoiceFilter, AllValuesFilter, DateFilter, DateFromToRangeFilter, CharFilter, ModelChoiceFilter, DurationFilter, MultipleChoiceFilter
from .models import *
from taggit.managers import TaggableManager

artist_list = []
for artist in Artist.objects.all():
    artist_list.append((artist.id, artist.name))


class MusicFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name='release_date', label='Year is greater than', lookup_expr='gte')
    # end_date = DateFilter(field_name='release_date', label='Year is less than', lookup_expr='lte')
    description = CharFilter(field_name = 'description', label='Description',lookup_expr='icontains')
    artist = MultipleChoiceFilter(field_name='artist', choices = artist_list, label= 'artist')
    release_date = DateFromToRangeFilter(field_name = 'release_date')
    # tags = TagsFilter

    # filter_overrides = {
    #     TaggableManager: {
    #          'filterset_class': AllValuesFilter,
    #          'extra': 'icontains'
    #     }
    # }

    class Meta:
        model = Music
        fields = ['released_by', 'curator']