from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_pk")
        return Contributor.objects.filter(project_id=project_id, user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj.project, user=request.user).exists()
