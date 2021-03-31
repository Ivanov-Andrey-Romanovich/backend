from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from .models import Blog, Post
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User



def get_blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    context = {'blogs': blogs}
    return render(request, 'labwork/index.html', context)


@login_required(login_url = '/lab/login')
def blog(request):
    if request.method == 'POST':
        return create_post(request)
    else:
        return render_blog(request)


def render_blog(request, additional_context = {}):
    b_id = 3
    blog = get_object_or_404(Blog, id = b_id)
    context = {
        'blog': blog,
        'posts': blog.post_set.order_by('-created_at'),
        **additional_context,
        }
    return render(request, 'labwork/index.html', context)

def create_post(request):
    blog = get_object_or_404(Blog, id = 3)
    subject = request.user.username
    text = request.POST['text']
    subject_error = None
    text_error = None
    if not subject or subject.isspace():
        subject_error = 'Please log in'
    if not text or text.isspace():
        text_error = 'Empty text form'
    if subject_error or text_error:
        error_context={
            'subject_error':subject_error,
            'text_error': text_error,
            'subject': subject,
            'text':text,
        }
        return render_blog(request, error_context)
    else:
        Post(blog_id = 3,subject = subject, text = text).save()
        return HttpResponseRedirect(reverse('blog_by_id',kwargs = {})) 


    

def log_in(request):
    if request.method == "POST":
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect(request.GET['next'])
            else:
                form.add_error('Invalid user')
    else:
        form = LoginForm()
    return render(request,'labwork/login.html',{'form':form})
    
def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            email = form.cleaned_data['email']
            user = authenticate(username = username,password = password)
            if User.objects.filter(username=username).exists():
                form.add_error('username','User already exists')
            elif password != password_again:
                form.add_error('password_again', 'Passwords missmatch')
            else:
                user = User.objects.create_user(username, email, password)
                blog = Blog.objects.create(author = user,title = "Andrey's Post")
                login(request,user)
                context = {
                    'blog': blog,
                    'posts': [],
                    }
                return render(request,'labwork/index.html',context)
    else: #GET
        form = RegistrationForm()
    return render(request,'labwork/signup.html',{'form':form})

def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)