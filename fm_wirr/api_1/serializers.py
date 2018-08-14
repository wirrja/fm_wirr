from .models import ScrobbleCard, Album, Artist, Song
from django.contrib.auth.models import User
from rest_framework import serializers


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            # 'url',
            "id",
            "title",
        )


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = (
            # 'url',
            "id",
            "title",
        )


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            "id",
            "name",
            # 'albums',
            # 'songs'
        )


class UserSerializer(serializers.ModelSerializer):
    # user = 'username'
    class Meta:
        model = User
        fields = ("id",)


class ScrobbleCardSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=False)
    artist = ArtistSerializer()
    album = AlbumSerializer(read_only=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ScrobbleCard
        fields = ("id", "date_post", "user", "date_listen", "song", "album", "artist")

    def create(self, validated_data):
        user = self.context["request"].user
        artist_name = validated_data.get("artist", {}).get("name")
        song_title = validated_data.get("song", {}).get("title")
        song_length = validated_data.get("song", {}).get("length")
        album_title = validated_data.get("album", {}).get("title")
        artist = Artist.objects.get_or_create(name=artist_name)[0]
        album = Album.objects.get_or_create(title=album_title, artist_id=artist.pk)[0]
        song = Song.objects.get_or_create(
            title=song_title.title(),
            length=song_length,
            artist_id=artist.pk,
            album_id=album.pk,
        )[0]
        date_listen = validated_data.get("date_listen")
        scrobble = ScrobbleCard.objects.create(
            album_id=album.pk,
            artist_id=artist.pk,
            song_id=song.pk,
            date_listen=date_listen,
            user=user,
        )
        return scrobble
