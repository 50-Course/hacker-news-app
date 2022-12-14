# Generated by Django 4.0.8 on 2022-10-10 10:32
from __future__ import annotations

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HNUser",
            fields=[
                (
                    "uid",
                    models.CharField(
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Unique User ID",
                    ),
                ),
                ("delay", models.IntegerField(default=0)),
                ("created", models.DateTimeField(auto_now=True)),
                ("karma", models.PositiveIntegerField()),
                ("submitted", models.JSONField(default=list)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("deleted", models.BooleanField(blank=True, default=False)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("job", "Job"),
                            ("story", "Story"),
                            ("comment", "Comment"),
                            ("poll", "Poll"),
                            ("pollopt", "Pollopt"),
                        ],
                        default="story",
                        max_length=40,
                    ),
                ),
                ("kids", models.JSONField(default=list)),
                ("dead", models.BooleanField(blank=True, default=False)),
                (
                    "time",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            2022, 10, 10, 10, 32, 20, 69974, tzinfo=utc
                        ),
                        null=True,
                    ),
                ),
                (
                    "by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="by_user",
                        to="api.hnuser",
                    ),
                ),
            ],
            options={
                "ordering": ("time",),
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.item",
                    ),
                ),
                ("parent", models.PositiveIntegerField(blank=True, null=True)),
                ("text", models.TextField(blank=True, null=True)),
            ],
            bases=("api.item",),
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.item",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        blank=True,
                        max_length=240,
                        null=True,
                        verbose_name="The Comment or Story or Poll",
                    ),
                ),
                ("url", models.URLField()),
                ("title", models.CharField(blank=True, max_length=40)),
            ],
            options={
                "verbose_name": "Job",
                "verbose_name_plural": "Jobs",
            },
            bases=("api.item",),
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.item",
                    ),
                ),
                ("descendants", models.JSONField(default=list)),
                ("score", models.PositiveIntegerField(blank=True, null=True)),
                ("parts", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                ("text", models.TextField(blank=True, null=True)),
            ],
            bases=("api.item",),
        ),
        migrations.CreateModel(
            name="Story",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.item",
                    ),
                ),
                (
                    "descendants",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("score", models.PositiveIntegerField(blank=True, null=True)),
                ("url", models.URLField()),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=40, verbose_name="Story Title"
                    ),
                ),
            ],
            bases=("api.item",),
        ),
        migrations.CreateModel(
            name="PollOption",
            fields=[
                (
                    "item_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.item",
                    ),
                ),
                (
                    "score",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.poll",
                    ),
                ),
            ],
            bases=("api.item",),
        ),
    ]
