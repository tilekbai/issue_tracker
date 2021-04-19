from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from tracker.models import Project
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, CreateView
from django.views.generic import CreateView, DetailView, ListView
from .forms import MyUserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin



class RegisterView(CreateView):
    model = User
    template_name = 'registration/user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('tracker:issue-list')
        return next_url
        

class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) 