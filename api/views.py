from __future__ import annotations

import logging

from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.models.models import Comment
from api.models.models import HNUser
from api.models.models import Item
from api.models.models import Job
from api.models.models import Poll
from api.models.models import PollOption
from api.models.models import Story
from api.permissions import was_created_internally
from api.serializers import BaseItemSerializer
from api.serializers import CommentSerializer
from api.serializers import JobSerializer
from api.serializers import StorySerializer
from api.serializers import UserSerializer


logger = logging.getLogger(__name__)


class GetLatestNewsAPIView(ListCreateAPIView):
    """
    Retrieves Latest News from our DB
    """

    queryset = Item.objects.all()
    serializer_class = BaseItemSerializer
    filterset_fields = ["type", "time", "by"]

    def create(self, request, *args, **kwargs):
        news_data = request.data
        # news_data['was_created_internally'] = False
        serializer = self.get_serializer(
            data=news_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):

        serializer.save()


class UpdateorDeleteNewsAPIView(RetrieveUpdateDestroyAPIView):
    """
    Updates or deletes a News
    """

    queryset = Item.objects.all()
    serializer_class = BaseItemSerializer
    # permission_classes = [was_created_internally, ]
    lookup_field = "id"


class StoriesViewset(viewsets.ModelViewSet):
    """
    Viewset for Stories.

    Methods:
        recent_stories (function)
    """

    queryset = Story.objects.all()
    serializer_class = StorySerializer


class CommentViewset(viewsets.ModelViewSet):
    """
    Viewset for Comment.

    Methods:
        recent_stories (function)
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class JobViewset(viewsets.ModelViewSet):
    """
    Viewset for Jobs.

    Methods:JobViewset, StoriesViewset
        recent_stories (function)
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Users ViewSet

    Args:
        viewsets (_type_): _description_
    """

    queryset = HNUser.objects.all()
    serializer_class = UserSerializer
