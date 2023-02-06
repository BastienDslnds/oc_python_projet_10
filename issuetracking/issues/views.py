from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.shortcuts import get_object_or_404

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
    IsAuthor,
    IsProjectContributor,
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


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthor]

    def get_queryset(self):
        user = self.request.user
        # un utilisateur ne doit pas être autorisé à accéder à un projet
        # pour lequel il n'est pas ajouté en tant que contributeur
        return Project.objects.filter(
            Q(author_user=user.id) | Q(contributors__user_id=user.id)
        )

    def create(self, request, *args, **kwargs):
        project = request.data
        project['author_user'] = request.user.id
        serializer = ProjectListSerializer(data=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data
        data['author_user'] = request.user.id
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        self.check_object_permissions(request, project)
        serializer = ProjectListSerializer(project, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        self.check_object_permissions(request, project)
        project.delete()
        return Response(
            {'message': 'The contributor has been deleted'},
            status=status.HTTP_200_OK,
        )


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorSerializer

    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(request, project)
        contributor = request.data
        contributor['project'] = self.kwargs['project_pk']
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

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(request, project)
        contributor = get_object_or_404(
            Contributor,
            project=self.kwargs['project_pk'],
            user=self.kwargs['pk'],
        )
        contributor.delete()
        return Response(
            {'message': 'The contributor has been deleted'},
            status=status.HTTP_200_OK,
        )


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthor, IsProjectContributor]

    def get_queryset(self):
        # Les problèmes du projet doivent être visibles
        # par tous les contributeurs et l'auteur
        contributor_projects = Project.objects.filter(
            Q(contributors__user_id=self.request.user)
            | Q(author_user=self.request.user)
        )
        return Issue.objects.filter(
            project=self.kwargs['project_pk'],
            project__in=contributor_projects,
        )

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsProjectContributor()]
        else:
            return [IsAuthor()]

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        self.check_object_permissions(request, project)
        issue = request.data
        issue['project'] = self.kwargs['project_pk']
        issue['author_user'] = request.user.id

        # Si l'utilisateur ne renseigne pas l'assignee
        # alors il est en assignee user par défaut
        if not issue.get('assignee_user'):
            issue['assignee_user'] = request.user.id
        serializer = IssueListSerializer(data=issue)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=self.kwargs['pk'])
        self.check_object_permissions(request, issue)
        data = request.data
        data['project'] = self.kwargs['project_pk']
        data['author_user'] = request.user.id
        if not data.get('assignee_user'):
            data['assignee_user'] = request.user.id
        serializer = IssueListSerializer(issue, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=self.kwargs['pk'])
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response(
            {'message': 'The issue has been deleted'},
            status=status.HTTP_200_OK,
        )


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsProjectContributor()]
        else:
            return [IsAuthor()]

    def is_issue_exist_on_project(self):
        is_issue_exist = Issue.objects.filter(
            id=self.kwargs['issue_pk'], project=self.kwargs['project_pk']
        )
        if is_issue_exist:
            return True
        return False

    def get_queryset(self):
        contributor_projects = Project.objects.filter(
            Q(contributors__user_id=self.request.user)
            | Q(author_user=self.request.user)
        )
        # il faut que le projet de l'issue reliée aux commentaires
        # soit dans les projets accessibles par le user authentifié
        return Comment.objects.filter(
            issue_id=self.kwargs['issue_pk'],
            issue__in=Issue.objects.filter(project__in=contributor_projects),
            issue__project_id=self.kwargs['project_pk'],
        )

    def create(self, request, *args, **kwargs):
        is_issue_exist = self.is_issue_exist_on_project()
        if not is_issue_exist:
            return Response(
                {'message': "The issue doesn't exist on this project"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
            self.check_object_permissions(request, project)
            comment = request.data
            comment['issue'] = self.kwargs['issue_pk']
            comment['author_user'] = request.user.id
            serializer = CommentSerializer(data=comment)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        self.check_object_permissions(request, comment)
        data = request.data
        data['issue'] = self.kwargs['issue_pk']
        data['author_user'] = request.user.id

        serializer = CommentSerializer(comment, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(
            {'message': 'The comment has been deleted'},
            status=status.HTTP_200_OK,
        )
