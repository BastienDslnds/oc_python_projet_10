from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author_user',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author_user',
            'issues',
            'contributors',
        ]

    def get_issues(self, instance):

        queryset = instance.issues.all()

        serializer = IssueListSerializer(queryset, many=True)

        return serializer.data

    def get_contributors(self, instance):

        queryset = instance.contributors.all()

        serializer = ContributorSerializer(queryset, many=True)

        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'priority',
            'project',
            'status',
            'author_user',
            'assignee_user',
            'created_time',
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'desc',
            'tag',
            'priority',
            'project_id',
            'status',
            'author_user',
            'assignee_user',
            'created_time',
            'comments',
        ]

    def get_comments(self, instance):

        queryset = instance.comments.all()

        serializer = CommentSerializer(queryset, many=True)

        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'description',
            'author_user',
            'issue',
            'created_time',
        ]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']
