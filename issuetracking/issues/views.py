from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentSerializer,
)
from .models import Project, Contributor, Issue, Comment
from .permissions import (
    IsAuthorOrReadOnly,
    IsProjectContributor,
    IsAuthorToHandleContributors,
)


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if (
            self.action == 'retrieve'
            and self.detail_serializer_class is not None
        ):
            return self.detail_serializer_class
        return super().get_serializer_class()


# class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

#     serializer_class = ProjectListSerializer
#     detail_serializer_class = ProjectDetailSerializer

#     def get_queryset(self, *args, **kwargs):
#         user = self.request.user
#         print(self.request)
#         print(user.id)
#         return Project.objects.filter(
#             Q(author_user=user.id) | Q(contributors__user_id=user.id)
#         )


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        # un utilisateur ne doit pas être autorisé à accéder à un projet pour lequel il n'est pas ajouté en tant que contributeur
        return Project.objects.filter(
            Q(author_user=user.id) | Q(contributors__user_id=user.id)
        )

    def create(self, request):
        project = request.data
        # author_user du projet est automatiquement renseigné
        # pas besoin de renseigner le champ dans le body de la requête
        project['author_user'] = request.user.id
        print(project)
        serializer = ProjectListSerializer(data=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorSerializer

    permission_classes = [
        IsAuthorToHandleContributors,
    ]

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        contributor = request.data
        print(contributor)
        if not (
            Contributor.objects.filter(
                user=request.user, project=self.kwargs['project_pk']
            ).exists()
        ):
            serializer = ContributorSerializer(data=contributor)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'message': 'The user is already a contributor of the project'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# class IssueViewset(MultipleSerializerMixin, ModelViewSet):

#     serializer_class = IssueListSerializer
#     detail_serializer_class = IssueDetailSerializer

#     def get_queryset(self):
#         return Issue.objects.filter(project_id=self.kwargs['project_pk'])


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly,
        IsProjectContributor,
    ]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def post(self, request):
        issue = request.data
        # issue['author_user'] = request.user

        # # par défaut, si l'utilisateur ne renseigne pas l'assignee alors il est en assignee user
        # if not issue['assignee_user']:
        #     issue['assignee_user'] = request.user

        serializer = ProjectListSerializer(issue)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly,
        IsProjectContributor,
    ]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])
