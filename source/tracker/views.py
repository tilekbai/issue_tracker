from django.shortcuts import render
from django.views.generic import View, TemplateView
from tracker.models import Issue

# Create your views here.

class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        return render(request, 'index.html', context={'issues': issues})