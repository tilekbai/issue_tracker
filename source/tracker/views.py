from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, DetailView
from tracker.base_views import FormView as CustomFormView, CustomListView

from tracker.models import Issue, Status, Issue_type, Project
from tracker.forms import IssueForm, IssueDeleteForm, SearchForm

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
    

class IssueView(TemplateView):
    template_name = "issue_view.html"
    
    def get_context_data(self, **kwargs):
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        return super().get_context_data(**kwargs)


class Issue_createView(CustomFormView):
   template_name = 'issue_create.html'
   form_class = IssueForm

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
       return reverse('issue-view', kwargs={'pk': self.issue.pk})


class Issue_updateView(FormView):
    template_name = 'issue_update.html'
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

    def get_initial(self):
        initial = {}
        for key in 'summary', 'description', 'status':
            initial[key] = getattr(self.issue, key)
        initial['issue_type'] = self.issue.issue_type.all()
        return initial

    def form_valid(self, form):
        issue_type = form.cleaned_data.pop('issue_type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.issue, key, value)
        self.issue.save()
        self.issue.issue_type.set(issue_type)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-view', kwargs={'pk': self.issue.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, pk=pk)
        

class Issue_deleteView(View):
    def get(self, request, *args, **kwargs):
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        form = IssueDeleteForm()
        return render(request, 'issue_delete.html', context={'issue': kwargs ["issue"], 'form': form})

    def post(self, request, *args, **kwargs):
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        form = IssueDeleteForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['summary'] != kwargs ["issue"].summary:
                form.errors['summary'] = ['Названия задач не совпадают']
                return render(request, 'issue_delete.html', context={'issue': kwargs ["issue"], 'form': form})

            kwargs ["issue"].delete()
            return redirect('issue-list')
        return render(request, 'issue_delete.html', context={'issue': kwargs ["issue"], 'form': form})


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project