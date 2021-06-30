from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

release_types = (
    ('LP', 'LP'),
    ('EP', 'EP'),
    ('Single', 'Single'),
    ('Song', 'Song')
)

class Artist(models.Model):
    name = models.CharField(blank =True, max_length=100)
    location = models.CharField(blank =True, max_length=50)
    bio = models.CharField(blank =True, max_length=1000)
    bandcamp_link = models.URLField(blank =True )
    spotify_link = models.URLField(blank =True )
    instagram_link = models.URLField(blank =True )
    discogs_link = models.URLField(blank =True )
    spotify_embed = models.CharField(blank =True, max_length=1000)
    tags = TaggableManager()

    def __str__(self):
        return self.name



class Curator(models.Model):
    name = models.CharField(blank =True, max_length=100)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(blank =True, max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Submission(models.Model):
    artist_name = models.CharField(blank =True, max_length=100)
    link = models.URLField(blank =True )
    comments = models.CharField(blank =True, max_length=1000)
    social_media_link = models.URLField(blank =True )
    you = models.CharField(blank =True, max_length=3, choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    ))

class Music(models.Model):
    name = models.CharField(blank =True, max_length=100)
    release_year = models.IntegerField(blank =True)
    release_date = models.DateField(blank =True)
    released_by = models.CharField(blank =True, max_length=1000)
    description = models.CharField(blank =True, max_length=1000)
    spotify_embed = models.CharField(blank =True, max_length=1000)
    bandcamp_embed = models.CharField(blank =True, max_length=1000)
    discogs_link = models.URLField(blank =True )
    genre = models.CharField(blank =True, max_length=1000)
    release_type = models.CharField(blank =True, max_length=10, choices = release_types)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)
    comments = models.ForeignKey(Comment, null = True, blank=True, on_delete=models.CASCADE)
    tags = TaggableManager()


    def __str__(self):
        return (f'{self.name}, {self.release_year}')

