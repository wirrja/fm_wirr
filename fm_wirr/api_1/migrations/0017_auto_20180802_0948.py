# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-02 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api_1", "0016_auto_20180802_0945")]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="album_cover",
            field=models.ImageField(
                default="noimage.png", max_length=1000, upload_to="static/media/"
            ),
        )
    ]
