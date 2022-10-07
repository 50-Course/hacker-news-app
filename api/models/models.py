#  models.py
from __future__ import annotations

"""
This module provides a set of models for Hacker News.

Models here, are represented as Python Dataclasses, \
    serialized into Django Model Fields with the help \
        of a data class serializer.

"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.fields import ArrayField


_Type = (
    ("JOB", "Job"),
    ("STORY", "Story"),
    ("COMMENT", "Comment"),
    ("POLL", "Poll"),
    ("POLLOPT", "Pollopt"),
)
"""
Enumeration of the type of the model.
"""


class Base(models.Model):
    """
    Base model for Hacker News.

    Arguments:
        id (int) - The item's unique id.

        deleted (bool) - if the item is deleted.

        type (`job` | `story` | `comment` | `poll` | `pollopt`) \
            - the type of the item.

        by (str) - the username of the item's author.

        time (datetime.time) - creation time of this item.

        dead (bool) - if the item is dead.

        kids (Sequence[int]) - the ids of the iem's comment, arranged \
            in display order.
    """

    item_id = models.IntegerField(
        _("Item Id"),
        unique=True,
        null=True,
        blank=True,
    )

    deleted = models.BooleanField(
        blank=True,
        default=False,
        help_text="is this item deleted? ",
    )
    type = models.CharField(
        choices=_Type, max_length=12, null=False, blank=False
    )
    by = models.ForeignKey(
        "User", on_delete=models.CASCADE, max_length=40, blank=True, null=True
    )
    time = models.DateTimeField(auto_now=True, blank=True, null=True)
    dead = models.BooleanField(default=False, blank=True, null=True)
    kids = ArrayField(base_field=models.IntegerField(blank=True, null=True))

    class Meta:
        abstract = True
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['id', 'type'],
        #         name='unique_item'
        #     )
        # ]
        ordering = ["kids"]


class User(Base):
    """
    User model Class for Hacker News.

    Args:
        id (str) - The user's unique username. Case-sensitive.

        delay (datetime.time) - delay in minutes, between \
            a comment's creation and its visibility to other users.

        created (datetime.date) - the creation date of the user

        karma (number) - the user's karma

        about (str) - an optional, self description of a user

        submitted (Sequence[int]) - list of the user's stories \
            polls and comments.
    """

    id = models.CharField(
        _("Unique User ID"),
        max_length=8,
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
    )
    delay = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True, blank=False, null=False)
    karma = models.PositiveIntegerField(blank=False, null=False)
    submitted = ArrayField(models.IntegerField(blank=True))

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.UniqueConstraint(
                fields=["id", "created", "karma"], name="unique_user_id"
            )
        ]

    def __str__(self) -> str:
        return f"User: {self.id}, Karma: {self.karma}"


class Job(Base):
    """
    Job model for Hacker News.

    Arguments:
        text (str) - the comment, story or poll text HTML.

        url (str) - the url of the story.

        title (str) - the title of the Story, Poll or Job
    """

    text = models.CharField(
        _("The Comment", "Story", "Poll"),
        max_length=240,
        blank=True,
        null=True,
    )
    url = models.URLField()
    title = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self) -> str:
        return self.text


class Story(Base):
    """
    Story model for Hacker News.

    Arguments:
        descendants (int) - In the case of stories \
            or polls, the total comment count
        score (int) - The story score or the votes \
            for a pollopt
    """

    descendants = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    url = models.SlugField()
    title = models.CharField(
        _("Story Title"), max_length=40, null=True, blank=True
    )

    def __str__(self) -> str:
        return super().__str__({"title": self.title, "url": self.url})


class Comment(Base):
    """
    Comment model for Hacker News.

    Args:
        parent (int) - the item's parent. For comments, \
            either another comment or the relevant story. \
                For pollopts, the relevant poll
        text (str) - the comment, story or poll text HTML.
    """

    parent = models.PositiveIntegerField(null=False)
    text = models.TextField(blank=True, null=True)


class PollOption(Base):
    """
    PollOption model for Hacker News.

    Args:
        parent (int) - the item's parent. For comments, \
            either another comment or the relevant story. \
                For pollopts, the relevant poll
        score (int) = the story's score or the votes for a \
            pollopt
    """

    parent = models.ForeignKey("Poll", on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0, blank=True)
    title = models.CharField(null=True, blank=True, max_length=100)


class Poll(Base):
    """
    Poll model for Hacker News.

    Arguments:
        parts (Sequence[int]) - a list of related \
            pollopt, in display order
        descendants (int) - in the case of stories \
            or polls, the total comment count
        score (int) - the story score or the votes \
            for a pollopt
    """

    descendants = ArrayField(models.IntegerField(blank=True))
    score = models.PositiveIntegerField(blank=True)
    parts = models.PositiveIntegerField(blank=True)
    title = models.CharField(max_length=40, null=True)
    text = models.TextField(null=True, blank=True)
