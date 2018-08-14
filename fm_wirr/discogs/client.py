import django
import discogs_client
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
import requests
from django.conf import settings
from api_1.models import Album, Song, Artist
from discogs.settings import KEYS


class ClientError(ValueError):
    pass


class UnknownSongLength(ClientError):
    pass


class UnknownDatabaseField(ClientError):
    pass


class UnknownSearchKeyword(ClientError):
    pass


class EmptyValuesNotFound(ClientError):
    pass


class CreateFolderError(IOError):
    pass


def get_sec(strings):
    """Calculate song`s length in seconds"""
    sep_strings = strings.split(":")
    if len(sep_strings) == 3:
        h, m, s = sep_strings
        result = int(h) * 3600 + int(m) * 60 + int(s)
        return result

    elif len(sep_strings) == 2:
        m, s = sep_strings
        result = int(m) * 60 + int(s)
        return result
    else:
        # raise UnknownSongLength(sep_strings)
        # print(strings)
        pass


class SearchContent:
    """
    search_keywords в теле класса-родитея однотипные,
    список будет пополняться в make_search_args
    при создании класса-потомка в search_keywords
    необходимо указывать нужные поля, они пригодятся при поиске.
    'key': 'key' одинаковые.
    В случае, когда при поиске необходим неименованный аргумент,
    нужно писать 'key': True
    """

    query = None
    search_keywords = {"artist": True, "release_title": "release_title", "type": "type"}
    media_path = settings.MEDIA_ROOT

    def get_content(self):
        """
        Формируем args и kwargs для метода поиска
        search_content(). Из двух dict формируем list
        args и dict kwargs
        :return yield search result from discogs api
        """
        query = self.query_checker(self.query)
        if query:
            for album in query:
                try:
                    main_keywords = dict()
                    main_keywords["artist"] = album.artist.name
                    main_keywords["album"] = album.title
                    main_keywords["release_title"] = album.title
                    main_keywords["type"] = "master"
                    # main_keywords["format"] = "album"
                except:
                    main_keywords = dict()
                    main_keywords["artist"] = album.name
                    main_keywords["type"] = "band"
                args = list()
                kwargs = dict()
                for key, value in self.search_keywords.items():
                    if value is not True:
                        kwargs[key] = main_keywords.get(key)
                    else:
                        args.append(main_keywords.get(key))

                # print(args, kwargs)

                yield self.search_content(args, kwargs), album.artist.name, album.title

    @staticmethod
    def search_content(args, kwargs):
        dc = discogs_client.Client(
            user_agent=KEYS["user_agent"], user_token=KEYS["personal_token"]
        )
        try:
            answer = dc.search(*args, **kwargs)
            answer = list(answer)[0]

        except:
            kwargs["type"] = "release"
            answer = dc.search(*args, **kwargs)
            try:
                answer = list(answer)[0]
                if answer:
                    return answer
            except:
                pass
        return answer

    @staticmethod
    def query_checker(query):
        if query.exists():
            return query
        else:
            return None
            # raise EmptyValuesNotFound(query)

    def __repr__(self):
        return "%s" % self.__class__.__name__


class DownloadCovers(SearchContent):
    query = Album.objects.filter(album_cover="noimage.png")

    def fill_content(self):

        for album in self.get_content():
            try:
                cover_link = album[0].data["cover_image"]
                artist = album[1]
                title = album[2]
                path_media = self._save_content(cover_link, artist, title)
                self._update_database(artist, title, path_media)
            except:
                pass

    def _save_content(self, cover_link, artist, title):
        path_album = os.path.join(self.media_path, artist, title)
        path_cover = path_album + "/cover.jpg"
        path_media = os.path.join(artist, title, "cover.jpg")
        if not os.path.exists(path_album):
            try:
                os.makedirs(path_album)
            except:
                raise CreateFolderError

        with open(path_cover, "wb") as cover:
            web_cover = requests.get(cover_link)
            cover.write(web_cover.content)

            return path_media

    def _update_database(self, artist, title, path_media):
        self.query.filter(artist__name=artist, title=title).update(
            album_cover=path_media
        )


class DownloadThumbs(SearchContent):
    media_path = settings.MEDIA_ROOT
    query = Album.objects.filter(album_thumb="noimage_thumb.png")

    def fill_content(self):

        for album in self.get_content():
            try:
                thumb_link = album[0].data["thumb"]
                artist = album[1]
                title = album[2]
                path_media = self._save_content(thumb_link, artist, title)
                self._update_database(artist, title, path_media)
            except:
                pass

    def _save_content(self, thumb_link, artist, title):
        path_album = os.path.join(self.media_path, artist, title)
        path_thumb = path_album + "/thumb.jpg"
        path_media = os.path.join(artist, title, "thumb.jpg")
        if not os.path.exists(path_album):
            try:
                os.makedirs(path_album)
            except:
                raise CreateFolderError
        with open(path_thumb, "wb") as thumb:
            web_thumb = requests.get(thumb_link)
            thumb.write(web_thumb.content)

            return path_media

    def _update_database(self, artist, title, path_media):
        self.query.filter(artist__name=artist, title=title).update(
            album_thumb=path_media
        )


class DownloadTracklist(SearchContent):
    query = Album.objects.filter(album_tracklist="{}")

    def fill_content(self):
        for album in self.get_content():
            try:
                tracklist_obj = album[0].tracklist
                artist = album[1]
                title = album[2]
                tracklist = [x.title for x in tracklist_obj]
                self._fill_database(artist, title, tracklist)
            except:
                pass

    def _fill_database(self, artist, title, tracklist):

        self.query.filter(artist__name=artist, title=title).update(
            album_tracklist=tracklist
        )


class DownloadBandPhoto(SearchContent):
    query = Artist.objects.filter(artist_photo="noimage.png")
    search_keywords = {"artist": True, "type": "band"}

    def fill_content(self):
        for artist in self.get_content():
            print(artist)


# DownloadCovers().fill_content()
# DownloadThumbs().fill_content()
# DownloadTracklist().fill_content()
# DownloadBandPhoto().fill_content()


# from pprint import pprint


# def search_content(args, kwargs):
#     dc = discogs_client.Client(
#         user_agent=KEYS["user_agent"], user_token=KEYS["personal_token"]
#     )
#     answer = dc.search(*args, **kwargs)
#     return answer


# args = ["Slowdive"]
# kwargs = {"release_title": "Slowdive", "type": "master"}
#
# answer = search_content(args, kwargs)
# pprint(answer[0].data)
