from django.contrib.auth import login, authenticate
from django.views.generic.list import ListView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from api_1.models import ScrobbleCard, Album, Artist
import time
from .forms import SignUpForm


def get_date_range(past):
    """Calculate date and time for last 7,30,365 days
    statistics, return timestamp or None
    """
    time_now_ts = int(time.time())
    return {
        "week": lambda: time_now_ts - 86400 * 7,
        "month": lambda: time_now_ts - 86400 * 30,
        "year": lambda: time_now_ts - 86400 * 365,
    }.get(past, lambda: None)()


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


class BasicView(ListView):
    """Базовый класс с навигационным меню"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["username"] = self.request.user
        else:
            context["username"] = "Guest"

        return context


class IndexView(BasicView):
    template_name = "index.html"
    model = ScrobbleCard
    context_object_name = "last_albums"

    def get_queryset(self):
        qs = super().get_queryset()
        # today_midnight = datetime.datetime.combine(datetime.date.today(), datetime.time())
        # today_ts = int(datetime.datetime.timestamp(today_midnight))
        # last_mon = today_midnight - datetime.timedelta(days=today_midnight.weekday(), weeks=1)
        # last_mon_ts = int(datetime.datetime.timestamp(last_mon))

        qs = qs.raw(
            """
             SELECT 1 as id, title, album_cover, api_1_artist.name,
             min(api_1_scrobblecard.date_post) as date_post
             FROM api_1_scrobblecard
             INNER JOIN api_1_album ON api_1_scrobblecard.album_id = api_1_album.id
             INNER JOIN api_1_artist ON api_1_album.artist_id = api_1_artist.id
             GROUP BY title, album_cover, name
             ORDER BY date_post DESC LIMIT 12;
            """
        )

        return qs


class HomeView(BasicView):
    model = ScrobbleCard
    template_name = "home.html"

    context_object_name = "last_tracks"

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs["user"]
        username = get_object_or_404(User.objects.filter(username=username))
        now = int(time.time())
        week = get_date_range("week")
        # month = get_date_range("month")
        # year = get_date_range("year")
        # Последние 10 треков, прослушанных пользователем
        recent_tracks = qs.raw(
            """
                SELECT 1 as id, to_timestamp(api_1_scrobblecard.date_listen) as time,
                api_1_artist.name as band,
                api_1_song.title as title,
                api_1_album.album_thumb as album_thumb,
                auth_user.username as username
                FROM api_1_scrobblecard
                INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
                INNER JOIN api_1_artist on api_1_scrobblecard.artist_id = api_1_artist.id
                INNER JOIN api_1_song ON api_1_scrobblecard.song_id = api_1_song.id
                INNER JOIN api_1_album ON api_1_scrobblecard.album_id = api_1_album.id
                WHERE username = '%s'
                ORDER BY time DESC;

                """
            % username
        )

        recent_week_tracks = qs.raw(
            """
            SELECT 1 as id, name, api_1_song.title, count(api_1_scrobblecard.song_id) as count
            FROM api_1_scrobblecard INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
            INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
            INNER JOIN api_1_song ON api_1_scrobblecard.song_id = api_1_song.id
            WHERE username = '%s' AND date_listen BETWEEN %d AND %d
            GROUP BY api_1_song.title, name
            ORDER BY count DESC LIMIT 10;
            """
            % (username, week, now)
        )
        qs = (list(recent_tracks), list(recent_week_tracks))
        qs = list(qs)

        return qs


class HomeArtistsView(BasicView):
    template_name = "home_artists.html"
    model = ScrobbleCard
    context_object_name = "home_artists"
    # paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs["user"]
        username = get_object_or_404(User.objects.filter(username=username))
        now = int(time.time())
        week = get_date_range("week")
        all_artists = qs.raw(
            """
        SELECT 1 as id, api_1_artist.name as name, count(api_1_scrobblecard.artist_id) as count,
        api_1_artist.artist_photo as artist_photo
        FROM api_1_scrobblecard
        INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
        INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
        WHERE username = '%s'
        GROUP BY name, username, artist_photo
        ORDER BY count DESC;
        """
            % username
        )

        recent_seven_days = qs.raw(
            """
            SELECT 1 as id, api_1_artist.name as name, count(api_1_scrobblecard.song_id) as count,
            api_1_artist.artist_photo as artist_photo
            FROM api_1_scrobblecard INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
            INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
            WHERE username = '%s' AND date_listen BETWEEN '%d' AND '%d'
            GROUP BY name, artist_photo
            ORDER BY count DESC LIMIT 10;
            """
            % (username, week, now)
        )
        qs = (list(all_artists), list(recent_seven_days))
        qs = list(qs)

        return qs


class HomeAlbumsView(BasicView):
    template_name = "home_albums.html"
    model = ScrobbleCard
    context_object_name = "home_albums"

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs["user"]
        username = get_object_or_404(User.objects.filter(username=username))
        now = int(time.time())
        week = get_date_range("week")
        all_albums = qs.raw(
            """
            SELECT 1 as id, api_1_album.title as album_title, count(api_1_scrobblecard.album_id) as count,
            api_1_artist.name as artist_name, api_1_album.album_thumb as album_thumb
            FROM api_1_scrobblecard
            INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
            INNER JOIN api_1_album ON api_1_scrobblecard.album_id = api_1_album.id
            INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
            
            WHERE username = '%s'
            GROUP BY username, album_title, album_thumb, artist_name
            ORDER BY count DESC;
        """
            % username
        )
        recent_week_albums = qs.raw(
            """
            SELECT  1 as id, api_1_album.title as album_title, count(api_1_scrobblecard.album_id) as count,
            api_1_artist.name as artist_name, api_1_album.album_thumb as album_thumb
            FROM api_1_scrobblecard
            INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
            INNER JOIN api_1_album ON api_1_scrobblecard.album_id = api_1_album.id
            INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
            WHERE username = '%s' AND date_listen BETWEEN '%d' and '%d'
            GROUP BY username, album_title, album_thumb, artist_name
            ORDER BY count DESC LIMIT 10;
            
            """
            % (username, week, now)
        )
        qs = (list(all_albums), list(recent_week_albums))
        qs = list(qs)

        return qs


class HomeAlbumsViewChange(BasicView):
    template_name = "change_album.html"
    model = Album
    context_object_name = "change_album"

    def __init__(self):
        super().__init__()
        self.album = None
        self.artist = None

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs["user"]
        username = get_object_or_404(User.objects.filter(username=username))
        self.album = get_object_or_404(Album, title=self.kwargs["album"])
        self.artist = Artist.objects.get(albums__title=self.kwargs["album"])
        qs = qs.filter(title=self.album).order_by("title")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album"] = self.album
        context["artist"] = self.artist
        return context


class HomeSongsView(BasicView):
    template_name = "home_songs.html"
    model = ScrobbleCard
    context_object_name = "home_songs"

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs["user"]
        username = get_object_or_404(User.objects.filter(username=username))
        week = get_date_range("week")
        now = int(time.time())
        # top all tracks for all time
        all_tracks = qs.raw(
            """
                SELECT 1 as id, api_1_song.title as song_title, count(api_1_scrobblecard.song_id) as count,
                api_1_artist.name as artist_name, api_1_album.album_thumb
                FROM api_1_scrobblecard
                INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
                INNER JOIN api_1_song ON api_1_scrobblecard.song_id = api_1_song.id
                INNER JOIN api_1_album ON api_1_song.album_id = api_1_album.id
                INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
                WHERE username = '%s'
                GROUP BY song_title, username, artist_name, album_thumb
                ORDER BY count DESC;
            """
            % username
        )

        recent_week_tracks = qs.raw(
            """
                SELECT 1 as id, name, api_1_song.title, count(api_1_scrobblecard.song_id) as count
                FROM api_1_scrobblecard INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
                INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
                INNER JOIN api_1_song ON api_1_scrobblecard.song_id = api_1_song.id
                WHERE username = '%s' AND date_listen BETWEEN %d AND %d
                GROUP BY api_1_song.title, name
                ORDER BY count DESC LIMIT 10;
                """
            % (username, week, now)
        )

        qs = (list(all_tracks), list(recent_week_tracks))
        qs = list(qs)

        return qs


class MusicArtistsView(BasicView):
    model = Artist
    context_object_name = "music_artists"
    template_name = "music_artists.html"
    # paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by("name")
        return qs


class MusicAlbumsView(BasicView):
    model = Album
    context_object_name = "music_albums"
    template_name = "music_albums.html"
    # paginate_by = 10

    def __init__(self):
        super().__init__()
        self.artist = None

    def get_queryset(self):
        qs = super().get_queryset()
        # remove .title()
        self.artist = get_object_or_404(Artist, name=self.kwargs["artist"])

        qs = qs.filter(artist__name=self.artist).order_by("title")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artist"] = self.artist
        return context


class UserProfile(BasicView):
    model = ScrobbleCard
    template_name = "user_profile.html"
    context_object_name = "user_data"

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.kwargs["user"]
        username = get_object_or_404(User.objects.filter(username=username))

        qs = qs.raw(
            """
            SELECT 1 as id, api_1_artist.name as artist_name,
                   api_1_album.title as album_title
            
            FROM api_1_scrobblecard
            INNER JOIN auth_user ON api_1_scrobblecard.user_id = auth_user.id
            INNER JOIN api_1_artist ON api_1_scrobblecard.artist_id = api_1_artist.id
            INNER JOIN api_1_album ON api_1_scrobblecard.album_id = api_1_album.id
            WHERE username = '%s'
            group by artist_name, album_title
            order by artist_name;
            """
            % username
        )

        return qs
