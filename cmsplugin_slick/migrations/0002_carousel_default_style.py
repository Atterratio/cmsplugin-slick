# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_slick', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='default_style',
            field=models.BooleanField(default=True, verbose_name='Use default style'),
        ),
    ]
