from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField

from django.contrib.admin import ModelAdmin


class Artist(models.Model):
    name = models.CharField(db_index=True, unique=False, max_length=90)

    artist_description = models.CharField(
        unique=False, default="No Description", max_length=4096
    )
    artist_photo = models.ImageField(
        unique=False, default="noimage.png", max_length=2048
    )

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(db_index=True, unique=False, max_length=90)
    album_cover = models.ImageField(
        unique=False, default="noimage.png", max_length=1000
    )
    album_thumb = models.ImageField(
        unique=False, default="noimage_thumb.png", max_length=1000
    )
    album_video = models.CharField(unique=False, default="No Video", max_length=1000)
    album_description = models.CharField(
        unique=False, default="No Description", max_length=1024
    )
    album_tracklist = ArrayField(
        models.CharField(blank=True, max_length=10000),
        blank=True,
        # null=True,
        default="{}",
    )
    album_genre = models.CharField(
        db_index=True, unique=False, default="music", max_length=100
    )
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(db_index=True, unique=False, max_length=90)
    length = models.PositiveIntegerField(blank=True, null=True)
    artist = models.ForeignKey(Artist, related_name="songs", on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name="songs", on_delete=models.CASCADE)
    position = models.CharField(unique=False, max_length=10, null=True, blank=True)
    video = models.CharField(unique=False, max_length=1000, default="No video")
    lyrics = models.CharField(unique=False, max_length=2000, default="No lyrics")

    def __str__(self):
        # minutes, seconds = self.length // 60, self.length % 60
        return self.title


class ScrobbleCard(models.Model):
    user = models.ForeignKey(User, related_name="usernames", on_delete=models.CASCADE)
    artist = models.ForeignKey(
        Artist, related_name="scrobble_cards_artists", on_delete=models.CASCADE
    )
    album = models.ForeignKey(
        Album, related_name="scrobble_cards_albums", on_delete=models.CASCADE
    )
    song = models.ForeignKey(
        Song, related_name="scrobble_cards_songs", on_delete=models.CASCADE
    )
    # время публикации скроббла
    date_post = models.DateTimeField(db_index=True, auto_now_add=True)
    date_listen = models.BigIntegerField(
        db_index=True, validators=[MinValueValidator(1125932400)]
    )

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
            self.date_post,
            self.date_listen,
            self.artist,
            self.album,
            self.song,
            self.user,
        )
