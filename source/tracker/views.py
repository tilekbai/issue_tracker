from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.utils.http import urlencode
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from tracker.base_views import FormView as CustomFormView, CustomListView

from tracker.models import Issue, Status, Issue_type, Project
from tracker.forms import IssueForm, IssueDeleteForm, SearchForm, ProjectForm, SearchProjectForm, UsersListForm

# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Issue
    context_object_name = "issues"
    ordering = ("-created_at", "summary")
    paginate_by = 10
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()

        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_data:
            queryset = queryset.filter(
                Q(summary__icontains = self.search_data) |
                Q(description__icontains = self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data["search_value"]
        return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form

        if self.search_data:
            context["query"] = urlencode({"search_value": self.search_data})

        return context


class IssueView(DetailView):
    model = Issue
    template_name = 'issue_view.html'


class Issue_createView(PermissionRequiredMixin, CustomFormView):
    template_name = 'issue_create.html'
    model = Issue   
    form_class = IssueForm
    context_object_name = 'issue'
    permission_required = 'tracker.add_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, id=self.kwargs.get('pk'))
        project = issue.project
        return  self.request.user in project.user_id.all() and super().has_permission()

    def form_valid(self, form):
        data = {}
        issue_type = form.cleaned_data.pop('issue_type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                data[key] = value
        self.issue = Issue.objects.create(**data)
        self.issue.issue_type.set(issue_type)
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('tracker:issue-view', kwargs={'pk': self.issue.pk})


class Issue_updateView(PermissionRequiredMixin, UpdateView):    
    model = Issue
    template_name = 'issue_update.html'
    form_class = IssueForm
    context_object_name = 'issue'
    permission_required = 'tracker.change_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, id=self.kwargs.get('pk'))
        project = issue.project
        return  self.request.user in project.user_id.all() and super().has_permission()

    def get_success_url(self):
        return reverse('tracker:issue-view', kwargs={'pk': self.object.pk})
        

class Issue_deleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'issue_delete.html'
    model = Issue
    context_object_name = 'issue'
    success_url = reverse_lazy('tracker:issue-list')
    permission_required = 'tracker.delete_issue'

    def has_permission(self):
        issue = get_object_or_404(Issue, id=self.kwargs.get('pk'))
        project = issue.project
        return  self.request.user in project.user_id.all() and super().has_permission()


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project


class ProjectsListView(ListView):
    template_name = "projects/projects_list.html"
    model = Project
    context_object_name = "projects"
    ordering = ("name")
    paginate_by = 10
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()

        return super(ProjectsListView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains = self.search_data) |
                Q(description__icontains = self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data["search_value"]
        return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form

        if self.search_data:
            context["query"] = urlencode({"search_value": self.search_data})

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/create_project.html'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        project = form.save(commit = False)
        project.save()
        project.user_id.set([self.request.user])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('tracker:project-view', kwargs={'pk': self.object.pk})


class ProjectIssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    template_name = 'issue_create.html'
    form_class = IssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'tracker:project-view',
            kwargs={'pk': self.kwargs.get('pk')}
        )

    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'tracker.change_project'
    
    def get_success_url(self):
        return reverse('tracker:project-view', kwargs={'pk': self.object.pk})


class Project_deleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'projects/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('tracker:projects-list')
    permission_required = 'tracker.delete_project'


class Project_Userlist_changeView(PermissionRequiredMixin, UpdateView):
    form_class = UsersListForm
    model = Project
    template_name = "projects/project_user_create.html"
    context_object_name = "project"
    permission_required = "tracker.project_user_add"

    def has_permission(self):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        return self.request.user in project.user_id.all() and super().has_permission()

    def form_valid(self, form):
        user_id = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("tracker:project-view", kwargs={'pk': self.object.pk})

    