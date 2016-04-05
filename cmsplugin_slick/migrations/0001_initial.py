# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.folder
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaroselImageFolder',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='cms.CMSPlugin', auto_created=True)),
                ('title', models.CharField(null=True, max_length=255, blank=True, verbose_name='Title')),
                ('folder', filer.fields.folder.FilerFolderField(null=True, to='filer.Folder', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='cms.CMSPlugin', auto_created=True)),
                ('title', models.CharField(max_length=60, blank=True, verbose_name='Title')),
                ('infinite', models.BooleanField(default=True, verbose_name='Infinite')),
                ('speed', models.IntegerField(default=300, verbose_name='Speed')),
                ('dots', models.BooleanField(default=True, verbose_name='Dots')),
                ('arrows', models.BooleanField(default=True, verbose_name='Arrows')),
                ('slides_to_show', models.IntegerField(default=1, verbose_name='Slides to show')),
                ('slides_to_scroll', models.IntegerField(default=1, verbose_name='Slides to scroll')),
                ('autoplay', models.BooleanField(default=False, verbose_name='Autoplay')),
                ('autoplay_speed', models.IntegerField(null=True, blank=True, verbose_name='Autoplay speed')),
                ('pause_on_hover', models.BooleanField(default=True, verbose_name='Pause on hover')),
                ('pause_on_dots_hover', models.BooleanField(default=False, verbose_name='Pause on dots hover')),
                ('fade', models.BooleanField(default=False, verbose_name='Fade animation')),
                ('center_mode', models.BooleanField(default=False, verbose_name='Center mode')),
                ('center_padding', models.CharField(max_length=10, blank=True, verbose_name='Center padding')),
                ('variable_width', models.BooleanField(default=False, verbose_name='Variable Width')),
                ('vertical', models.BooleanField(default=False, verbose_name='Vertical')),
                ('rigth_to_left', models.BooleanField(default=False, verbose_name='Right to left')),
                ('classes', models.TextField(blank=True, verbose_name='Css classes')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CarouselBreakpoint',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('breakpoint', models.IntegerField(verbose_name='Breakpoint resolution')),
                ('slides_to_show', models.IntegerField(default=1, verbose_name='Slides to show')),
                ('slides_to_scroll', models.IntegerField(default=1, verbose_name='Slides to scroll')),
                ('carousel', models.ForeignKey(related_name='breakpoints', to='cmsplugin_slick.Carousel', verbose_name='Carousel')),
            ],
        ),
        migrations.CreateModel(
            name='CarouselElementWrapper',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='cms.CMSPlugin', auto_created=True)),
                ('classes', models.TextField(blank=True, verbose_name='Css classes')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
