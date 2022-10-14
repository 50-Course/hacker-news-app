from __future__ import annotations

from django import forms

from api.models.models import Comment
from api.models.models import Item
from api.models.models import Job
from api.models.models import Poll
from api.models.models import PollOption
from api.models.models import Story


class BaseItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["type"]


class StoryForm(BaseItemForm):
    type = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={
                "placeholder": "type",
                "class": "form-control",
            }
        ),
        error_messages={
            "required": "Type is required. Please check again.",
            "invalid": "You have entered an invalid type",
        },
    )

    # Metadata
    class Meta(BaseItemForm.Meta):
        model = Story
        fields = BaseItemForm.Meta.fields + ["title", "url"]


class JobsForm(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        model = Job
        fields = BaseItemForm.Meta.fields + ["text", "url", "title"]


class PollsForm(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        model = Poll
        fields = BaseItemForm.Meta.fields + ["score", "title", "text"]


class PollOptForm(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        model = PollOption
        fields = BaseItemForm.Meta.fields + ["title"]


class CommentForm(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        model = Comment
        fields = BaseItemForm.Meta.fields + ["text"]
