# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-02 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api_1", "0013_auto_20180802_0929")]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="album_thumb",
            field=models.ImageField(
                default="noimage_thumb.png", max_length=1000, upload_to="static/media/"
            ),
        ),
        migrations.AlterField(
            model_name="artist",
            name="artist_photo",
            field=models.ImageField(
                default="noimage.png", max_length=1000, upload_to="static/media/"
            ),
        ),
    ]
