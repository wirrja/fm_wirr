from .models import Album, Artist, Song, ScrobbleCard
from rest_framework import viewsets, generics
from .serializers import (
    ArtistSerializer,
    AlbumSerializer,
    SongSerializer,
    ScrobbleCardSerializer,
)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class ScrobbleCardViewSet(viewsets.ModelViewSet):
    queryset = ScrobbleCard.objects.all()
    serializer_class = ScrobbleCardSerializer


class ScrobbleCardView(generics.ListAPIView):
    serializer_class = ScrobbleCardSerializer

    def get_queryset(self):
        user = self.kwargs["user"]
        return ScrobbleCard.objects.filter(user__username=user)
