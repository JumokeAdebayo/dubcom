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
from .models import Post
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
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
    logger.debug(form)
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


class PostDetailView(DetailView):
   model = Post
   template_name = 'ecommerce/post_detail.html'

def get_context_data(self, *arg, **kwargs):
             context = super().get_context_data(**kwargs)
             form = CommentForm()
             context['form'] = form  # Your comment form
             return context

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

# def post_detail(request, slug):
#     template_name = 'ecommerce/post_detail.html'
#     post = get_object_or_404(Post, Slug = slug)
#     comments = post.comments.filter(Active=True, Parent__isnull=True)
#     new_comment = None
#     #Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():

#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     return render(request, 'ecommerce/post_detail.html', {'post': post,
#                                            'comments': comments,
#                                            'new_comment': new_comment,
#                                            'comment_form': comment_form})

    

    # if request.method == 'post':
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         Parent_obj = None
    #         try:
    #             Parent_id = int(request.POST.get('Parent_id'))
    #         except:
    #             Parent_id = None
    #         if Parent_id:
    #             Parent_obj = Comment.objects.get(id=Parent_id)
    #             if Parent_obj:
    #                 reply_comment = comment_form.save(commit=False)
    #                 reply_comment.Parent = Parent_obj
    #             new_comment = comment_form.save(commit=False)
    #             new_comment.Post = post
    #             new_comment.save()
    #             return redirect('ecommerce:post_detail', slug)
    #         else:
    #             comment_form = CommentForm()


    # return render(request, 'ecommerce/post_detail.html', {'post':post, 'comment':comments, 'comment_form':comment_form})

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

@method_decorator([login_required, allowed_users(allowed_roles=['admin'])], name='dispatch')
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
