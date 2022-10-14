from __future__ import annotations

from rest_framework.routers import SimpleRouter

from .views import CommentViewset
from .views import JobViewset
from .views import StoriesViewset

router = SimpleRouter()

router.register(r"comments", CommentViewset)
router.register(r"jobs", JobViewset)
router.register(r"stories", StoriesViewset)
