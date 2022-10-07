from __future__ import annotations

from rest_framework.serializers import ModelSerializer

from api.models.models import Base
from api.models.models import Comment
from api.models.models import Job
from api.models.models import Poll
from api.models.models import PollOption
from api.models.models import Story


class BaseClassSerializer(ModelSerializer):
    class Meta:
        model = Base
        fields = "__all__"


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        extra_kwargs = {"id": "read-only"}


class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll


class PollOptSerializer(ModelSerializer):
    class Meta:
        model = PollOption


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment


class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
