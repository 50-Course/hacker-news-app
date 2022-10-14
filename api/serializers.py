from __future__ import annotations

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer

from api.lib.time import UnixTimeField
from api.models.models import Comment
from api.models.models import HNUser
from api.models.models import Item
from api.models.models import Job
from api.models.models import Poll
from api.models.models import PollOption
from api.models.models import Story


MAX_FIELDS_LENGTH = 40
MAX_ALLOWED_DEPTH = 5
"""This is the maximum number of comments, that can be \
    retrived on a single post or max. related stories \
        associated with a single one."""


class BaseItemSerializer(ModelSerializer):
    by = serializers.PrimaryKeyRelatedField(read_only=True)
    time = UnixTimeField()

    class Meta:
        model = Item
        fields = "__all__"
        depth = 1


class UserSerializer(ModelSerializer):
    class Meta:
        model = HNUser
        fields = "__all__"
        exclude = ["uid"]
        read_only_fields = ["uid"]


class JobSerializer(ModelSerializer):
    """
    Handles conversion of Job Data to python \
        primitives (back 'n' forth).
    """

    by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        extra_kwargs = {"id": "read-only"}
        depth = MAX_ALLOWED_DEPTH


class PollSerializer(ModelSerializer):
    r"""
    Handles conversion of UserPoll Data to python \def delete(self, instance, id)
        primitives (back 'n' forth).

    """
    by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"
        exclude = ["id"]
        depth = MAX_ALLOWED_DEPTH


class PollOptSerializer(ModelSerializer):
    """
    Converts Poll options to native python objects
    """

    by = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = PollOption


class CommentSerializer(ModelSerializer):
    """
    Handles conversion of Job Data to python \
        primitives (back 'n' forth).
    """

    by = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = Comment
        depth = MAX_ALLOWED_DEPTH
        exclude = ["id"]


class StorySerializer(ModelSerializer):
    class Meta:
        model = (Story,)
        depth = MAX_ALLOWED_DEPTH
        exclude = ["id"]
