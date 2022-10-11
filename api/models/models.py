from __future__ import annotations

"""
This module provides a set of models for Hacker News.

Models here, are represented as Python Dataclasses, \
    serialized into Django Model Fields with the help \
        of a data class serializer.

"""
#  models.py


from logging import getLogger
from typing import Dict
from django.utils import timezone


from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer
from django.urls import reverse
import requests
from django.contrib.auth.models import AbstractUser

from rest_framework import status
from django.conf import settings

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


logger = getLogger(__name__)

User = get_user_model()

_Type = (
    ("job", "Job"),
    ("story", "Story"),
    ("comment", "Comment"),
    ("poll", "Poll"),
    ("pollopt", "Pollopt"),
)
"""
Enumeration of the type of the model.
"""

BASE_URL = settings.HACKER_NEWSAPI_URI
"""Endpoint for interacting with """


# class Base(models.Model):
#     """
#     Base model for Hacker News.

#     Arguments:
#         id (int) - The item's unique id.

#         deleted (bool) - if the item is deleted.

#         type (`job` | `story` | `comment` | `poll` | `pollopt`) \
#             - the type of the item.

#         by (str) - the username of the item's author.

#         time (datetime.time) - creation time of this item.

#         dead (bool) - if the item is dead.

#         kids (Sequence[int]) - the ids of the iem's comment, arranged \
#             in display order.
#     """

#     id = models.IntegerField(
#         _("Item Id"),
#         unique=True,
#         null=False,
#         primary_key=True
#     )

#     deleted = models.BooleanField(
#         blank=True,
#         default=False,
#         help_text="is this item deleted? ",
#     )
#     type = models.CharField(
#         choices=_Type, max_length=12, null=False, blank=False
#     )
#     by = models.CharField(max_length=40, blank=True, null=False)
#     # by = models.ForeignKey(to='User'HTTP_201_CREATED,
#     #                           on_delete=models.CASCADE, related_name='by_user')
#     time = models.DateTimeField(auto_now=True, blank=True, null=True)
#     dead = models.BooleanField(default=False, blank=True, null=True)
#     kids = models.JSONField(default=list)
#     was_created_internally = models.BooleanField(default=False)

#     class Meta:
#         ordering = ["kids", 'time']
#         permissions = [
#             ('was_created_internally', 'was_created_internally')
#         ]

#     def __str__(self) -> str:
#         return f'{self.id}. Type: {self.type}'


class HNUser(models.Model):
    """
    User model Class for Hacker News.

    Args:
        id (str) - The user's unique username. Case-sensitive.

        delay (datetime.time) - delay in minutes, between \
            a comment's creation and its visibility to other users.

        created (datetime.date) - the creation date of the user

        karma (number) - the user's karma

        about (str) - an optional, self description of a user

        submitted (Iterable[int]) - list of the user's stories \
            polls and comments.
    """

    uid = models.CharField(
        _("Unique User ID"), max_length=25, primary_key=True, unique=True
    )
    user = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE
    )
    delay = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    karma = models.PositiveIntegerField()
    submitted = models.JSONField(default=list)

    USERNAME_FIELD = "uid"

    REQUIRED_FIELDS = ["uid"]

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"Hacker: {self.id}, current karma streak: {self.karma}"

    @staticmethod
    def retrieve_profile_from_db(uid: int):
        """
                Called after fetching user data from API.

                Args:
                    uid (int): the unique user id

                Returns:
                    QuerySet: A single object instance in the database
        cls
                @TODO: Move this method into a model manager.
        """
        return get_object_or_404(HNUser, pk=uid)

    def fetch_user_details(self, uid: str) -> dict:
        """
        Fetch user details from Hacker News Public API.

        Args:
            uid (int) - the user's uid
        Returns:
            data (Dict) - Json data fetched from their API.
        """
        url = f"{BASE_URL}/user/{uid}.json"
        try:
            response = requests.request("GET", url=url)
        except ConnectionError:
            logger.info(
                f"Error fetching data from API. "
                f"Please check your internet connection."
            )
            # instead of reeturning an empty object we could \
            # return objct in the db
            # return {}
            return HNUser.retrieve_profile_from_db(uid)

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            return data


class Item(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # deleted, type, kids, by, time, dead, kids
    deleted = models.BooleanField(default=False)
    type = models.CharField(
        choices=_Type, max_length=40, blank=True, default=_Type[1][0]
    )
    kids = models.JSONField(default=list)
    dead = models.BooleanField(default=False)
    time = models.DateTimeField(blank=True, null=True, default=timezone.now())
    by = models.ForeignKey(
        to=HNUser, on_delete=models.CASCADE, related_name="by_user", null=True
    )

    class Meta:
        ordering = ["time"]

    def __str__(self) -> str:
        return f"{self.id}. Type: {self.type}"

    def get_type(self) -> models.Model:
        """Display the item type in our template.

        Returns:
            models.Model: Returns a Django Model \
                that can be interfaced by Django's ORM.
        """
        model_type_mapping = {
            "story": Story,
            "comment": Comment,
            "poll": Poll,
            "pollopt": PollOption,
            "job": Job,
        }
        model_cls = model_type_mapping.get(self.type)
        return model_cls.objects.get(id=self.id)

    def get_absolute_url(self) -> str:
        return reverse("newsapp:get-items", kwargs={"id": self.id})


class Job(Item):
    """
    Job model for Hacker News.

    Arguments:
        text (str) - the comment, story or poll text HTML.

        url (str) - the url of the story.

        title (str) - the title of the Story, Poll or Job
    """

    text = models.CharField(
        _("The Comment or Story or Poll"),
        max_length=240,
        blank=True,
        null=True,
    )
    url = models.URLField()
    title = models.CharField(max_length=40, blank=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self) -> str:
        return self.text

    def save(self, *args, **kwargs) -> None:
        self.type = "job"
        return super().save(*args, **kwargs)


class Story(Item):
    """
    Story model for Hacker News.

    Arguments:
        descendants (int) - In the case of stories \
            or polls, the total comment count
        score (int) - The story score or the votes \
            for a pollopt
    """

    descendants = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField()
    title = models.CharField(_("Story Title"), max_length=40, blank=True)

    def __str__(self) -> str:
        return f"Story: {self.title}. Type: {self.type}"

    def save(self, *args, **kwargs):
        self.type = "story"
        return super().save(**args, **kwargs)


class Comment(Item):
    """
    Comment model for Hacker News.

    Args:
        parent (int) - the item's parent. For comments, \
            either another comment or the relevant story. \
                For pollopts, the relevant poll
        text (str) - the comment, story or poll text HTML.
    """

    parent = models.PositiveIntegerField(null=True, blank=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Comment: {self.text} on {self.parent}"

    def save(self, *args, **kwargs) -> None:
        self.type = "comment"
        return super().save(*args, **kwargs)


class Poll(Item):
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

    # descendants = ArrayField(models.IntegerField(blank=True))
    descendants = models.JSONField(default=list)
    score = models.PositiveIntegerField(blank=True, null=True)
    parts = models.PositiveIntegerField(blank=True, null=True)
    title = models.CharField(max_length=40, blank=True, null=True)
    text = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        self.type = "poll"
        return super().save(*args, **kwargs)


class PollOption(Item):
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
    score = models.PositiveIntegerField(default=0, null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs) -> None:
        self.type = "pollopt"
        return super().save(*args, **kwargs)
