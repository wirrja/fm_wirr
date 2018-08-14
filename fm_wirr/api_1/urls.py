from django.conf.urls import url, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r"artists", views.ArtistViewSet)
router.register(r"albums", views.AlbumViewSet)
router.register(r"songs", views.SongViewSet)
router.register(r"scrobbles", views.ScrobbleCardViewSet)


urlpatterns = [
    url(r"", include(router.urls)),
    url("^user/(?P<user>.+)/library/$", views.ScrobbleCardView.as_view()),
]
