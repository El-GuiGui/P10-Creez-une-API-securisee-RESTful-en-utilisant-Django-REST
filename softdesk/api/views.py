from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from .models import Project, Contributor, Issue, Comment, UserProfile
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsContributor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from django.contrib.auth.models import User


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination pour les résultats de l'API.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Récupère les projets de l'utilisateur courant.
        """
        user = self.request.user
        return Project.objects.filter(models.Q(author_user=user) | models.Q(contributors__user=user)).distinct()

    def perform_create(self, serializer):
        """
        Enregistre le projet avec l'utilisateur courant comme auteur.
        """
        serializer.save(author_user=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les contributeurs.
    """

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Récupère les contributions de l'utilisateur courant.
        """
        user = self.request.user
        return Contributor.objects.filter(user=user).distinct()

    def perform_create(self, serializer):
        """
        Enregistre un nouveau contributeur pour un projet.
        """
        project_id = self.request.data.get("project")
        user_id = self.request.data.get("user")

        try:
            project = Project.objects.get(id=project_id)
            user = User.objects.get(id=user_id)
            serializer.save(user=user, project=project)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les issues.
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Récupère les issues de l'utilisateur courant.
        """
        user = self.request.user
        return Issue.objects.filter(
            models.Q(author_user=user) | models.Q(assignee_user=user) | models.Q(project__contributors__user=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Enregistre une nouvelle issue avec l'utilisateur courant comme auteur.
        """
        serializer.save(author_user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Récupère les commentaires de l'utilisateur courant.
        """
        user = self.request.user
        return Comment.objects.filter(author_user=user).distinct()

    def perform_create(self, serializer):
        """
        Enregistre un nouveau commentaire avec l'utilisateur courant comme auteur.
        """
        serializer.save(author_user=self.request.user)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les profils utilisateur.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    """
    Vue pour l'enregistrement des utilisateurs.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = []


class UserDeleteView(APIView):
    """
    Vue pour la suppression des utilisateurs.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Supprime l'utilisateur courant.
        """
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
