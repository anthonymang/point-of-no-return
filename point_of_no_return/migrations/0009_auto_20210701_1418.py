# Generated by Django 3.2.4 on 2021-07-01 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_no_return', '0008_auto_20210630_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='artist_img',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='spotify_uri',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='music',
            name='album_art',
            field=models.URLField(blank=True, max_length=1000),
        ),
    ]
