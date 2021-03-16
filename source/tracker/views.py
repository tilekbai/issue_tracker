from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, TemplateView, RedirectView
from tracker.base_view import CustomFormView

from tracker.models import Issue, Status, Issue_type
from tracker.forms import IssueForm, IssueDeleteForm

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs['issues'] = Issue.objects.all()
        return super().get_context_data(**kwargs)


class IssueView(TemplateView):
    template_name = "issue_view.html"
    
    def get_context_data(self, **kwargs):
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        return super().get_context_data(**kwargs)


# class Issue_createView(View):
#     def get(self, request, *args, **kwargs):
#         form = IssueForm()
#         return render(request, 'issue_create.html', context={'form': form})


#     def post(self, request, *args, **kwargs):
#         form = IssueForm(data=request.POST)
#         if form.is_valid():
#             issue = Issue.objects.create(
#                 summary=form.cleaned_data.get('summary'),
#                 description=form.cleaned_data.get('description'),
#                 status=form.cleaned_data.get('status'),
#                 issue_type=form.cleaned_data.get('issue_type')
#             )
#             return redirect('issue-view', pk=issue.id)
            
#         return render(request, 'issue_create.html', context={'form': form})


class Issue_createView(View):

    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'issue_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():            
            issue_type=form.cleaned_data.pop('issue_type')

            issue = Issue.objects.create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
                status=form.cleaned_data.get('status'),
            )

            issue.issue_type.set(issue_type)
        return render(request, 'issue_view.html', context={'issue': issue})



class Issue_updateView(View):

    def get(self, request, *args, **kwargs):
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        form = IssueForm(initial={  
            'summary': kwargs ["issue"].summary,
            'description': kwargs ["issue"].description,
            'status': kwargs ["issue"].status,
            'issue_type': kwargs ["issue"].issue_type
        })
        return render(request, 'issue_update.html', context={'form': form, 'issue': kwargs ["issue"]})

    def post(self, request, *args, **kwargs):
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        form = IssueForm(data=request.POST) 
        if form.is_valid(): 
            kwargs ["issue"].summary = form.cleaned_data.get("summary")
            kwargs ["issue"].description = form.cleaned_data.get("description")
            kwargs ["issue"].status = form.cleaned_data.get("status")
            kwargs ["issue"].issue_type = form.cleaned_data.get("issue_type")
            kwargs ["issue"].save()
            return redirect('issue-view', pk=kwargs ["issue"].id)

        return render(request, 'issue_update.html', context={'form': form, 'issue': kwargs ["issue"]})


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
