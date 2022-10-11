from __future__ import annotations

from typing import Any
from typing import Dict

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .forms import BaseItemForm
from .forms import CommentForm
from .forms import JobsForm
from .forms import PollOptForm
from .forms import PollsForm
from .forms import StoryForm
from api.models.models import Comment
from api.models.models import Item
from api.models.models import Poll
from api.models.models import Story
from api.search.lookups import Search


class DisplayNewsView(TemplateView):
    """Display News Item on the frontend

    Args:
        TemplateView (_type_): _description_
    """

    template_name: str = "home.html"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: dict[str, Any]
    ) -> HttpResponse:
        """Returns a paginated response of news item.

        Args:
            request (httpRequest): request sent by the user

        """

        # If request contains search query
        # retrieve new by item or query or both
        # excluding the comments.
        query = request.GET.get("query")
        filter = request.GET.get("filters")

        if query or filter is None:
            qs = (
                Item.objects.all()
                .exclude(type="comment")
                .exclude(type="pollopt")
                .order_by("time")
            )
        elif query or filter:
            if query:
                search = Search()
                qs = search.full_match(query)

            filters = {"Story": "story", "Job": "job", "Poll": "poll"}

            if filter and filter in filters:
                qs = (
                    Item.objects.filter(filter=filter)
                    .exclude(type="comment")
                    .exclude(type="pollopt")
                    .order_by("time")
                )
        # Paginate QuerySet
        queryset = [q.get_type() for q in qs]
        paginator = Paginator(qs, 25)

        page = paginator.get_page(request.GET.get("page"))

        context = {
            "page_obj": page,
            "news": queryset,
            "story_form": StoryForm,
            "poll_form": PollsForm,
            "job_form": JobsForm,
        }
        return super().render_to_response(context=context)


def get_item_view(request, id: int, *args, **kwargs):
    if request.method == "GET":
        item = get_object_or_404(Item, id=id)
        obj = item.get_model_type()
        query = request.GET.get("search", None)

        if query:
            # import our search library
            search = Search()

            comments = search.comments(query, id)
        else:
            comments = Comment.objects.filter(parent__id=obj.id)
            return redirect(reverse("newsapp:get-items"))


@login_required
def profile_view(request, *args, **kwargs):
    """@TODO: Display the profile of a user."""
    pass


@login_required
def create_storyview(
    request: HttpRequest, *args: Any, **kwargs: dict[str, Any]
):
    """
    Create a new story.
    """
    form = StoryForm()

    if request.method == "POST":
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect(request, reverse("newsapp:list-items"))
        else:
            errors = form.errors
            return HttpResponse(errors)


@login_required
def create_jobview(request: HttpRequest, *args: Any, **kwargs: dict[str, Any]):
    """
    Create a new job.
    """
    form = JobsForm()

    if request.method == "POST":
        form = JobsForm(request.POST)
        if form.is_valid():
            jobs = form.save(commit=False)
            jobs.save()
            return redirect(request, reverse("newsapp:list-items"))
        else:
            errors = form.errors
            return HttpResponse(errors)
