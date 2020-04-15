import logging
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    TemplateView,
    DeleteView
)
from .models import Post, Comment
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from .filters import PostFilter 
from django.forms import inlineformset_factory


logger = logging.getLogger(__name__)


def home(request):

    if request.method == 'GET':

        myFilter = PostFilter(request.GET)
        context = {
            'posts': Post.objects.all(),
            'myFilter':myFilter
        }
        return render(request, 'ecommerce/home.html', context)


@login_required
@allowed_users(allowed_roles=['admin', 'Author'])
def post_create_view(request):
    
    template = 'ecommerce/post_form.html'
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect ('ecommerce-home')
    else:
        form = PostForm()

    context = {
        
        'form': form,
    }
    return render(request, 'ecommerce/post_form.html', context)
        

class PostListView(ListView):
    model = Post
    template_name = 'ecommerce/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4
    logger.debug(Post)


class UserPostListView(ListView):
    model = Post
    template_name = 'ecommerce/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    comments = Comment.objects.filter(post=post).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            body = request.POST.get('body')
            comment = Comment.objects.create(post=post, name=request.user.id, body=body)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form=CommentForm()

    context ={
            'post':post,
            'is_liked':is_liked,
            'total_likes':post.total_likes(),
            'comments':comments,
            'comment_form':comment_form,
    }
    return render(request, 'ecommerce/post_detail.html', context)


def post(self, request,*arg, **kwargs):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()
    context ={
            'form':form
    }
    return render(request, self.template_name, context)

@login_required
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
        is_liked = False
    else:
        post.likes.add(request.user.id)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


@method_decorator([login_required, allowed_users(allowed_roles=['admin', 'Author'])], name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@method_decorator([login_required, allowed_users(allowed_roles=['admin', 'Author'])], name='dispatch')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'ecommerce/about.html', {'title':'about'})


def commonuser(request):
    context = {}
    return render(request, 'ecommerce/commonuser.html', context)

    
# Create your views here.
