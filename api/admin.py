from django.contrib import admin

from api.models import models

@admin.register(models.Base):
class BaseAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Comment)
class CommentAdmin(admin.TabularInline):
    pass

@admin.register(models.Story)
class StoryAdmin(admin.TabularInline):
    pass

@admin.register(models.Poll)
class PollsAdmin(admin.TabularInline):
    pass

@admin.register(models.Polls)
class PollOPTAdmin(admin.TabularInline):
    pass
