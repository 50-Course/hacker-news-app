from __future__ import annotations

from django.contrib import admin

from api.models import models as m

# type: ignore
models = [m.Story, m.Comment, m.Poll, m.PollOption]
# type: ignore
admin.site.register(_ for _ in models)
