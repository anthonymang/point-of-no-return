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
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    bio = models.CharField(max_length=1000)
    bandcamp_link = models.URLField()
    spotify_link = models.URLField()
    instagram_link = models.URLField()
    twitter_link = models.URLField()
    discogs_link = models.URLField()
    spotify_embed = models.CharField(max_length=1000)
    bandcamp_embed = models.CharField(max_length=1000)
    tags = TaggableManager()

    def __str__(self):
        return self.name



class Curator(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Submission(models.Model):
    artist_name = models.CharField(max_length=100)
    link = models.URLField()
    comments = models.CharField(max_length=1000)
    social_media_link = models.URLField()
    you = models.CharField(max_length=3, choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    ))

class Music(models.Model):
    name = models.CharField(max_length=100)
    release_year = models.IntegerField()
    release_date = models.DateField()
    description = models.CharField(max_length=1000)
    spotify_embed = models.CharField(max_length=1000)
    bandcamp_embed = models.CharField(max_length=1000)
    discogs_link = models.URLField()
    genre = models.CharField(max_length=1000)
    release_type = models.CharField(max_length=10, choices = release_types)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curator = models.ForeignKey(Curator, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    tags = TaggableManager()


    def __str__(self):
        return self.name

