from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Project, Contributor, Issue, Comment


class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.project = Project.objects.create(
            title="Test Project", description="A test project", type="BACKEND", author_user=self.user
        )
        self.contributor = Contributor.objects.create(user=self.user, project=self.project)
        self.issue = Issue.objects.create(
            title="Test Issue",
            description="A test issue",
            project=self.project,
            author_user=self.user,
            assignee_user=self.user,
            priority="MEDIUM",
            tag="BUG",
            status="TODO",
        )
        self.comment = Comment.objects.create(issue=self.issue, author_user=self.user, description="A test comment")

    def test_create_project(self):
        data = {
            "title": "New Project",
            "description": "A new project",
            "type": "FRONTEND",
            "author_user": self.user.id,
        }
        response = self.client.post("/api/projects/", data)
        self.assertEqual(response.status_code, 201)

    def test_get_project(self):
        response = self.client.get(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_issue(self):
        data = {
            "title": "New Issue",
            "description": "A new issue",
            "project": self.project.id,
            "author_user": self.user.id,
            "assignee_user": self.user.id,
            "priority": "HIGH",
            "tag": "TASK",
            "status": "IN_PROGRESS",
        }
        response = self.client.post("/api/issues/", data)
        self.assertEqual(response.status_code, 201)

    def test_get_issue(self):
        response = self.client.get(f"/api/issues/{self.issue.id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        data = {"issue": self.issue.id, "author_user": self.user.id, "description": "A new comment"}
        response = self.client.post("/api/comments/", data)
        self.assertEqual(response.status_code, 201)

    def test_get_comment(self):
        response = self.client.get(f"/api/comments/{self.comment.id}/")
        self.assertEqual(response.status_code, 200)
