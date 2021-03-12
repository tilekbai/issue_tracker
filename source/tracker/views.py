from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from tracker.models import Issue

# Create your views here.

class IndexView(View):

    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        return render(request, "index.html", context={'issues': issues})

class IssueView(TemplateView):
    template_name = "issue_view.html"
    
    def get_context_data(self, **kwargs):
        print(kwargs)
        kwargs ["issue"] = get_object_or_404(Issue, id=kwargs.get("pk"))
        return super().get_context_data(**kwargs)