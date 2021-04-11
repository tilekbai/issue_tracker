from django.urls import path
from tracker.views import IndexView, IssueView, Issue_updateView, Issue_deleteView, Issue_createView, ProjectView, ProjectsListView, ProjectCreateView, ProjectIssueCreateView, ProjectUpdateView, Project_deleteView

app_name = "tracker"

urlpatterns = [
    path('', IndexView.as_view(), name="issue-list"),
    path('<int:pk>/add/', ProjectIssueCreateView.as_view(), name="issue-add"),
    path('<int:pk>/', IssueView.as_view(), name= "issue-view"),
    path('<int:pk>/update', Issue_updateView.as_view(), name="issue-update"),
    path('<int:pk>/delete', Issue_deleteView.as_view(), name='issue-delete'),
    path('<int:pk>/project', ProjectView.as_view(), name='project-view'),
    path('projects/list', ProjectsListView.as_view(), name="projects-list"),
    path('add_project/', ProjectCreateView.as_view(), name="project-add"),
    path('<int:pk>/updateproject', ProjectUpdateView.as_view(), name="project-update"),
    path('<int:pk>/project_delete', Project_deleteView.as_view(), name="project-delete")
]
