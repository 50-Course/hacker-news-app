"""
This module provides the implementation of search functionali.

The search functionalities are:

- The search functionalities are:
    * Search by Stories
    * Search by Jobs
    * Search by Polls
    and...
    you gerrit! 😎 ..
    * 'Full text' search

"""
####################
# @TODO: Implement ElasticSearch
#
####################
from __future__ import annotations

try:
    from typing import List
except ImportError:
    from typing_extensions import List
from django.db.models.query import Q, QuerySet
from api.models.models import Comment, Item, Job, Story, Poll


class Search:
    """
    This is the main class that is used to search for texts/

    It matches incoming query with data in the DB and \
        returns the matches/
    """

    def __init__(self, query):
        self.query = query

    def stories(self, text):
        if isinstance(self, text) is not str:
            return "Invalid search parameters"
        queryset = Story.objects.filter(
            Q(text__icontains=text)
            | Q(text__endswith=text)
            | Q(text__startwith=text)
            | Q(by__id__icontains=text)
        )
        return queryset

    def jobs(self, text):
        if isinstance(self, text) is not str:
            return "Invalid search parameters"
        queryset = Job.objects.filter(
            Q(title__icontains=text)
            | Q(title__endswith=text)
            | Q(text__icontains=text)
        )
        return queryset

    def polls(self, text):
        # Flters by title, text, time, by
        #
        #
        if isinstance(self, text) is not str:
            return "Invalid search parameters"
        queryset = Poll.objects.filter(
            Q(text__icontains=text)
            | Q(title__endswith=text)
            | Q(title__startwith=text)
            | Q(time__date=text)
            | Q(by__id=text)
        )
        return queryset

    def comments(self, text):
        """
        Returns a list of comments associated to an item.

        Args:
            text (str): Query been searched
        """
        qs = Comment.objects.all().filter(Q(text__icontains=text))

    def full_match(self, text) -> list[QuerySet]:
        """
        Returns a list of all texts that match the query
        """
        return [self.stories(text) + self.jobs(text) + self.polls(text)]
