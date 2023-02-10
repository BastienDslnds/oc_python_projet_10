"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import signup, login
from issues.views import (
    ProjectViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
)

router = routers.SimpleRouter()

router.register('projects', ProjectViewset, basename='project')

project_router = routers.NestedSimpleRouter(
    router, 'projects', lookup='project'
)
project_router.register('users', ContributorViewset, basename='project-users')

project_router.register('issues', IssueViewset, basename='project-issues')

project_issues_router = routers.NestedSimpleRouter(
    project_router, 'issues', lookup='issue'
)
project_issues_router.register(
    'comments', CommentViewset, basename='issue_comments'
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/signup/", signup, name='signup'),
    path("api/login/", login, name='login'),
    path("api/", include(router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(project_issues_router.urls)),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
]
