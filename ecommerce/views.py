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
from .forms import CommentForm, PostForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'ecommerce/home.html', context)

@allowed_users()
def post_list_view:
    PostListView.as_view()

class PostListView(ListView):
    model = Post
    template_name = 'ecommerce/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


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

def get_context_data(self, **kwargs):
             context = super().get_context_data(**kwargs)
             context['comment_form'] = comment_form()  # Your comment form
             return context

# def post_detail(request, slug):
#     template_name = 'ecommerce/post_detail.html'
#     post = get_object_or_404(Post, slug = slug)
#     comments = post.comments.filter(Active=True, Parent__isnull=True)
#     new_comment = None
#     Comment posted
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

#@allowed_users(allowed_roles=['admin', 'Author'])
# class PostCreateView(LoginRequiredMixin, CreateView, TemplateView):
#     model = Post
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


def postform(request):
    template = 'ecommerce/post_form.html'
    form = PostForm(request.POST or None)

    if form.is_valid():
        form.save()

    else:
        form = PostForm()

    context = {
            'form': form,
    }
    return render(request, 'ecommerce/post_form.html', context)

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
