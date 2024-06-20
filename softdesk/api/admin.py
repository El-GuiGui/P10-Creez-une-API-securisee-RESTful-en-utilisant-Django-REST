from django.contrib import admin
from .models import Project, Contributor, Issue, Comment, UserProfile

admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(UserProfile)
