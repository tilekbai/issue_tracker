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
from tracker.views import IndexView, IssueView, issue_create_view, issue_update_view, issue_delete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="issue-list"),
    path('<int:pk>/', IssueView.as_view(), name= "issue-view"),
    path('add/', issue_create_view, name='issue-add'),
    path('<int:pk>/update', issue_update_view, name='issue-update'),
    path('<int:pk>/delete', issue_delete_view, name='issue-delete'),
]
