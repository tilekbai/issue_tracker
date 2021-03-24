from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect

from tracker.forms import IssueForm
from tracker.models import Issue, Issue_type


class FormView(View):
    form_class = None
    template_name = None
    redirect_url = ''

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(self.get_redirect_url())


    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)


    def get_context_data(self, **kwargs):
        return kwargs


    def get_redirect_url(self):
        return self.redirect_url


class CustomListView(TemplateView):
    model = None
    context_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_name] = self.get_queryset
        return context

    def get_queryset(self):
        return self.model.objects.all()
