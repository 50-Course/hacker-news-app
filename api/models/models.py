#  models.py
"""
This module provides a set of models for Hacker News.

Models here, are represented as Python Dataclasses, \
    serialized into Django Model Fields with the help \
        of a data class serializer.

"""

from datetime import timezone
from email.policy import default
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.fields import ArrayField


_Type = \
    (
        ('JOB', 'Job'),
        ('STORY', 'Story'),
        ('COMMENT', 'Comment'),
        ('POLL', 'Poll'),
        ('POLLOPT', 'Pollopt'),
    )
    """
    Enumeration of the type of the model.
    """


class User(models.Model):
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
        _('Unique User ID'),
        unique=True,
        blank=False,
        null=False
    )
    delay = models.IntegerField(default=0)
    created = models.DateField(blank=False, null=False)
    karma = models.PositiveIntegerField(blank=False, null=False)
    submitted = ArrayField(
        models.IntegerField(blank=True)
    )

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint('id', 'created', 'karma')
        ]
        ordering = ['time']

    def __str__(self) -> str:
        return f'User: {self.id}, Karma: {self.karma}'

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
    id = models.PositiveIntegerField(
        _("Item Id"),
        serialize=True,
        editable=True,
        )

    deleted = models.BooleanField(
        blank=True,
        default=False,
        help_text="is this item deleted? ",

    )
    type = models.CharField(
        choices=_Type,
    )
    by = models.CharField(
        _('Author\'s Name'),
        max_length=40,
        blank=True,
        null=True
    )
    time = models.DateTimeField(auto_now=True, blank=True, null=True)
    dead = models.BooleanField(default=False, blank=True, null=True)
    kids = ArrayField(base_field=models.IntegerField(blank=True, null=True))

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                'id', 'type'
            )
        ]
        ordering = ['kids']


class Job(Base):
    """
    Job model for Hacker News.

    Arguments:
        text (str) - the comment, story or poll text HTML.

        url (str) - the url of the story.

        title (str) - the title of the Story, Poll or Job
    """
    text = models.CharField(
        _('The Comment', 'Story', 'Poll'),
        max_length=240,
        blank=True,
        null=True,
    )
    url = models.SlugField()
    title = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )


class Story(Job):
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


class Comment(Base):
    """
    Comment model for Hacker News.

    Args:
        parent (int) - the item's parent. For comments, \
            either another comment or the relevant story. \
                For pollopts, the relevant poll
        text (str) - the comment, story or poll text HTML.
    """
    parent = models.PositiveIntegerField()
    text = models.TextField()


class PollOption(Base):
    """
    PollOption model for Hacker News.

    Args:
        parent (int) - he item's parent. For comments, \
            either another comment or the relevant story. \
                For pollopts, the relevant poll
        score (int) = the story's score or the votes for a \
            pollopt
    """
    parent = models.PositiveIntegerField()
    score = models.PositiveIntegerField()


class Poll(Job):
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
    descendants = ArrayField(
        models.IntegerField(blank=True)
    )
    score = models.PositiveIntegerField()
    parts = models.PositiveIntegerField()
