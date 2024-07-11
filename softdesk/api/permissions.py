from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributor, Project, Issue


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est l'auteur de l'objet ou s'il a seulement des droits de lecture.
    """

    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions de l'utilisateur pour accéder à l'objet
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user


class IsContributor(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est un contributeur du projet.
    """

    def has_permission(self, request, view):
        """
        Vérifie les permissions de l'utilisateur pour accéder à une vue.
        """
        project_id = view.kwargs.get("project_pk")
        return Contributor.objects.filter(project_id=project_id, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions de l'utilisateur pour accéder à l'objet
        """
        return Contributor.objects.filter(project=obj.project, user=request.user).exists()


class IsProjectAuthor(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est l'auteur du projet.
    """

    def has_permission(self, request, view):
        """
        Vérifie les permissions de l'utilisateur pour accéder au projet.
        """
        project_id = view.kwargs.get("project_pk") or view.request.data.get("project")
        if not project_id:
            return False
        project = Project.objects.filter(id=project_id).first()
        return project and project.author_user == request.user

    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions de l'utilisateur pour accéder à l'objet
        """
        return obj.project.author_user == request.user


class IsContributorOrAuthor(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est contributeur ou auteur du projet.
    """

    def has_permission(self, request, view):
        """
        Vérifie les permissions de l'utilisateur pour accéder au projet.
        """
        if view.action in ["list", "retrieve"]:
            return True
        project_id = view.kwargs.get("project_pk") or view.request.data.get("project")
        if not project_id:
            project_id = view.get_object().project.id
        if not project_id:
            return False
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return False
        return (
            project.author_user == request.user
            or Contributor.objects.filter(project=project, user=request.user).exists()
        )

    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions de l'utilisateur pour accéder à l'objet
        """
        return (
            obj.project.author_user == request.user
            or Contributor.objects.filter(project=obj.project, user=request.user).exists()
        )


class IsCommentContributorOrAuthor(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est contributeur ou auteur du commentaire.
    """

    def has_permission(self, request, view):
        """
        Vérifie les permissions de l'utilisateur pour accéder au commentaire.
        """
        if view.action in ["list", "retrieve"]:
            return True
        if view.action == "create":
            issue_id = request.data.get("issue")
            if not issue_id:
                return False
            issue = Issue.objects.filter(id=issue_id).first()
            if not issue:
                return False
            project = issue.project
            return (
                project.author_user == request.user
                or Contributor.objects.filter(project=project, user=request.user).exists()
            )
        return True

    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions de l'utilisateur pour accéder à l'objet
        """
        if view.action in ["update", "partial_update", "destroy"]:
            return obj.author_user == request.user or obj.issue.project.author_user == request.user
        return True
