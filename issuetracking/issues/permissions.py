from rest_framework.permissions import BasePermission

from .models import Project


class IsAuthor(BasePermission):
    """Permission to check if the authenticated user is
    the author of the project or the issue or the comment."""

    message = "You're not allowed because you're not the author."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.author_user == request.user:
            return True
        return False


class IsProjectContributor(BasePermission):
    """Permission to check if the authenticated user is
    the author or a contributor of the project."""

    message = "You're not allowed because you're not the author or a contributor of the project."

    def project_contributor(self, request, obj):
        is_project_contributor = Project.objects.filter(
            contributors__project_id=obj.id,
            contributors__user_id=request.user.id,
        )
        is_project_author = obj.author_user == request.user
        return is_project_contributor or is_project_author

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if self.project_contributor(request, obj):
            return True
        return False
