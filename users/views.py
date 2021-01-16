from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib import messages

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("posts")
    template_name = "singup.html"



