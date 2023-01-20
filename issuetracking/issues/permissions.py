from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Project


class IsAuthorOrReadOnly(BasePermission):

    message = "You're not allowed because you're not the author."

    def has_permission(self, request, view):
        print("test 1")
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Si l'utilisateur connecté est l'auteur de l'objet étudié alors
        il peut faire GET, POST, PUT, DELETE etc
        Sinon, il peut seulement faire GET. et POST ?

        Args:
            request (_type_): _description_
            view (_type_): _description_
            obj (_type_): _description_

        Returns:
            _type_: _description_
        """
        print("test 2")
        print(obj)
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user


class IsProjectContributorOrAuthor(BasePermission):
    """Permission to check if the user is the author or a contributor of a project.
    In this case, the user can create an issue on the project.

    Args:
        BasePermission (_type_): _description_
    """

    message = ""

    def has_permission(self, request, view):
        print("test 3")
        print(request.user)
        print(request.user.is_authenticated)
        print(bool(request.user and request.user.is_authenticated))
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print("test 4")
        print(obj)
        is_project_contributor = Project.objects.filter(
            contributors__project_id=obj.id,
            contributors__user_id=request.user.id,
        )
        print(is_project_contributor)
        if is_project_contributor or obj.author_user == request.user:
            return True
        else:
            self.message = "You're not allowed because you're not the author or a contributor of the project."
            return False


# class IsAuthorToHandleContributors(BasePermission):

#     message = "Not allowed."

#     def has_permission(self, request, view):
#         print("test 5")
#         print(request.user)
#         print(request.user.is_authenticated)
#         print(bool(request.user and request.user.is_authenticated))
#         return bool(request.user and request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         # obj est un objet Contributor que la requête souhaite créer
#         # Je récupère le projet sur lequel la requête veut ajouter un contributeur
#         print("test 6")
#         project = get_object_or_404(Project, pk=obj.project_id)
#         print(project)
#         if request.method in SAFE_METHODS:
#             print("safe_methods")
#             return True
#         print(project.author_user)
#         print(request.user)
#         return project.author_user == request.user
