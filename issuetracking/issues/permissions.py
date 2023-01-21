from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Project


class IsAuthor(BasePermission):
    """Permission to check if the authenticated user is
    the author of the project or the issue or the comment."""

    message = "You're not allowed because you're not the author."

    def has_permission(self, request, view):
        print("test 1")
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print("test")
        if obj.author_user == request.user:
            return True
        elif request.method == 'POST':
            return True
        return False


class IsProjectContributor(BasePermission):

    message = "You're not allowed because you're not the author or a contributor of the project."

    def project_contributor(self, request, obj):
        is_project_contributor = Project.objects.filter(
            contributors__project_id=obj.id,
            contributors__user_id=request.user.id,
        )
        is_project_author = obj.author_user == request.user
        return is_project_contributor or is_project_author

    def has_permission(self, request, view):
        print("test 2")
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print("test")
        if self.project_contributor(request, obj):
            return True
        elif request.method in ['PUT', 'DELETE']:
            return True
        else:
            return False


# class MyPermission(BasePermission):

#     message = ""

#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         # boucle afin de tester si le user peut créer une issue ou un comment sur le projet
#         elif request.method == 'POST':
#             is_project_contributor = Project.objects.filter(
#                 contributors__project_id=obj.id,
#                 contributors__user_id=request.user.id,
#             ).exists()
#             if is_project_contributor or obj.author_user == request.user:
#                 return True
#             else:
#                 self.message = "You're not allowed because you're not the author or a contributor of the project."
#         # si le user est l'auteur du projet/issue/commentaire alors il peut tout faire
#         elif obj.author_user == request.user:
#             return True
#         else:
#             self.message = (
#                 "You're not allowed because you're not the author."
#             )
#             return False
