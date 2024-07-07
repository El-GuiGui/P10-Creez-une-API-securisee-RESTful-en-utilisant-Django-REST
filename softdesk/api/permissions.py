from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributor


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission pour vérifier si l'utilisateur est l'auteur de l'objet ou s'il a seulement des droits de lecture.
    """

    def has_object_permission(self, request, view, obj):
        """
        Vérifie les permissions de l'utilisateur sur un objet.
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
        Vérifie les permissions de l'utilisateur sur un objet.
        """
        return Contributor.objects.filter(project=obj.project, user=request.user).exists()
