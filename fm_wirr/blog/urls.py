from django.conf.urls import url
from django.contrib.auth import views as auth_views

# dev?
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    # Главная страница
    url(r"^$", views.IndexView.as_view(), name="index"),
    # Каталог музыки в базе
    url(r"^music/$", views.MusicArtistsView.as_view(), name="music_artists"),
    url(
        r"^music/(?P<artist>.+)/$", views.MusicAlbumsView.as_view(), name="music_albums"
    ),
    # Топы по категориям: Артист, Альбом, Трек. Для текущего пользователя
    url(r"^user/(?P<user>.+)/library/$", views.HomeView.as_view(), name="home"),
    url(
        r"^user/(?P<user>.+)/library/artists/$",
        views.HomeArtistsView.as_view(),
        name="home_artists",
    ),
    url(
        r"^user/(?P<user>.+)/library/albums/$",
        views.HomeAlbumsView.as_view(),
        name="home_albums",
    ),
    url(
        r"^user/(?P<user>.+)/library/songs/$",
        views.HomeSongsView.as_view(),
        name="home_songs",
    ),
    url(
        r"^user/(?P<user>.+)/library/albums/(?P<album>.+)/$",
        views.HomeAlbumsViewChange.as_view(),
        name="home_albums_change",
    ),
    url(r"^user/(?P<user>.+)/$", views.UserProfile.as_view(), name="home_user_profile"),
    # Служебные. Логин, регистрация, выход.
    url(r"^signup/$", views.signup, name="signup"),
    url(r"^login/$", auth_views.login, {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", auth_views.logout, name="logout"),
    # FAQ как работать с базой и скробблить
    # url(r'^faq/$', views.FAQView.as_view(), name='faq'),
    # Новости, изменения моделей, бложик автора
    # url(r'history/$', views.HistoryView.as_view(), name='history'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
