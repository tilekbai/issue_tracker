from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, TemplateView, RedirectView, FormView
from tracker.base_view import FormView as CustomFormView

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


# class Issue_updateView(View):

#     def get(self, request, *args, **kwargs):
#         kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
#         form = IssueForm(initial={  
#             'summary': kwargs ["issue"].summary,
#             'description': kwargs ["issue"].description,
#             'status': kwargs ["issue"].status,
#             'issue_type': kwargs ["issue"].issue_type.all()
#         })
#         return render(request, 'issue_update.html', context={'form': form, 'issue': kwargs ["issue"]})

#     def post(self, request, *args, **kwargs):
#         kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        
#         form = IssueForm(data=request.POST) 
                  
        

#         if form.is_valid(): 
#             issue_type=form.cleaned_data.pop('issue_type')

#             kwargs ["issue"].summary = form.cleaned_data.get("summary")
#             kwargs ["issue"].description = form.cleaned_data.get("description")
#             kwargs ["issue"].status = form.cleaned_data.get("status")
#             kwargs ["issue"].save()
            
#             kwargs ["issue"].issue_type.set(issue_type)
#             return redirect('issue-view', pk=kwargs ["issue"].id)

#         return render(request, 'issue_update.html', context={'form': form, 'issue': kwargs ["issue"]})


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
