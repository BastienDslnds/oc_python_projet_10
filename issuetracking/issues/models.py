from django.db import models
from django.conf import settings


class Project(models.Model):

    TYPE_CHOICES = (
        ('B', 'back-end'),
        ('F', 'front-end'),
        ('IOS', 'iOS'),
        ('A', 'Android'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, verbose_name='type'
    )
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class Issue(models.Model):

    PRIORITY_CHOICES = (
        ('FAIBLE', 'FAIBLE'),
        ('MOYENNE', 'MOYENNE'),
        ('ELEVEE', 'ELEVEE'),
    )
    STATUS_CHOICES = (
        ('A faire', 'A faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    )
    TAG_CHOICES = (
        ('BUG', 'BUG'),
        ('AMELIORATION', 'AMELIORATION'),
        ('TACHE', 'TACHE'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    tag = models.CharField(
        max_length=15, choices=TAG_CHOICES, verbose_name='tag'
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, verbose_name='priority'
    )
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name='issues'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name='status'
    )
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_issues',
    )
    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignee_issues',
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE, related_name='comments'
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name='contributors'
    )
    permission = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='permission'
    )
    role = models.CharField(max_length=20)
