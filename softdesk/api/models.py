from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid


class Project(models.Model):
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    IOS = "IOS"
    ANDROID = "ANDROID"
    PROJECT_TYPES = [
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=PROJECT_TYPES)
    author_user = models.ForeignKey(User, related_name="projects", on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_time"]


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, related_name="contributors", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} - {self.project.title}"
            if self.user
            else f"Utilisateur supprimé - {self.project.title}"
        )

    class Meta:
        ordering = ["-created_time"]


class Issue(models.Model):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    PRIORITY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    BUG = "BUG"
    FEATURE = "FEATURE"
    TASK = "TASK"
    TAG_CHOICES = [
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (TASK, "Task"),
    ]

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    STATUS_CHOICES = [
        (TODO, "To Do"),
        (IN_PROGRESS, "In Progress"),
        (FINISHED, "Finished"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name="issues", on_delete=models.CASCADE)
    author_user = models.ForeignKey(User, related_name="issues", on_delete=models.SET_NULL, null=True, blank=True)
    assignee_user = models.ForeignKey(
        User, related_name="assigned_issues", on_delete=models.SET_NULL, null=True, blank=True
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=TODO)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_time"]


class Comment(models.Model):
    issue = models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE)
    author_user = models.ForeignKey(User, related_name="comments", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.author_user.username} - {self.issue.title}"
            if self.author_user
            else f"Utilisateur supprimé - {self.issue.title}"
        )

    class Meta:
        ordering = ["-created_time"]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_delete, sender=User)
def anonymize_user_data(sender, instance, **kwargs):
    UserProfile.objects.filter(user=instance).delete()
