from config.celery import app
from discogs.client import DownloadCovers, DownloadThumbs, DownloadTracklist


@app.task
def get_tracklists():
    DownloadTracklist().fill_content()


@app.task
def get_covers():
    DownloadCovers().fill_content()


@app.task
def get_thumbs():
    DownloadThumbs().fill_content()
