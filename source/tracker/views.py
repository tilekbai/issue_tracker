from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, RedirectView

from tracker.models import Issue
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


def issue_create_view(request):
    

    if request.method == "GET":
        
        form = IssueForm()
        return render(request, 'issue_create.html', context={'form': form})
    elif request.method == "POST": 
        
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issue = Issue.objects.create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
                status=form.cleaned_data.get('status'),
                issue_type=form.cleaned_data.get('issue_type')
            )
            return redirect('issue-view', pk=issue.id)
            
        return render(request, 'issue_create.html', context={'form': form})


def issue_update_view(request, pk):
    
    issue = get_object_or_404(Issue, id=pk)

    if request.method == 'GET':
        form = IssueForm(initial={  
            'summary': issue.summary,
            'description': issue.description,
            'status': issue.status,
            'issue_type': issue.issue_type
        })
        return render(request, 'issue_update.html', context={'form': form, 'issue': issue})
    elif request.method == 'POST':
        form = IssueForm(data=request.POST) 
        if form.is_valid(): 
            issue.summary = form.cleaned_data.get("summary")
            issue.description = form.cleaned_data.get("description")
            issue.status = form.cleaned_data.get("status")
            issue.issue_type = form.cleaned_data.get("issue_type")
            issue.save()
            return redirect('issue-view', pk=issue.id)

        return render(request, 'issue_update.html', context={'form': form, 'issue': issue}) 
        

def issue_delete_view(request, pk):
    issue = get_object_or_404(Issue, id=pk)
    if request.method == 'GET':
        form = IssueDeleteForm()
        return render(request, 'issue_delete.html', context={'issue': issue, 'form': form})
    elif request.method == 'POST':
        form = IssueDeleteForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['summary'] != issue.summary:
                form.errors['summary'] = ['Названия задач не совпадают']
                return render(request, 'issue_delete.html', context={'issue': issue, 'form': form})

            issue.delete()
            return redirect('issue-list')
        return render(request, 'issue_delete.html', context={'issue': issue, 'form': form})

