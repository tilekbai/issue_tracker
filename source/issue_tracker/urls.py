"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from tracker.views import IndexView, IssueView, Issue_updateView, Issue_deleteView, Issue_createView, ProjectView, ProjectsListView, ProjectCreateView, ProjectIssueCreateView, ProjectUpdateView, Project_deleteView

from accounts.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="issue-list"),
    path('<int:pk>/add/', ProjectIssueCreateView.as_view(), name="issue-add"),
    path('<int:pk>/', IssueView.as_view(), name= "issue-view"),
    path('<int:pk>/update', Issue_updateView.as_view(), name="issue-update"),
    path('<int:pk>/delete', Issue_deleteView.as_view(), name='issue-delete'),
    path('<int:pk>/project', ProjectView.as_view(), name='project-view'),
    path('projects/list', ProjectsListView.as_view(), name="projects-list"),
    path('add_project/', ProjectCreateView.as_view(), name="project-add"),
    path('<int:pk>/updateproject', ProjectUpdateView.as_view(), name="project-update"),
    path('<int:pk>/project_delete', Project_deleteView.as_view(), name="project-delete"),
    path('accounts/login/', login_view, name="login"),
    path('accounts/logout/', logout_view, name="logout"),
]
