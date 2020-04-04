from django.urls import path
from .views import (
	PostListView, 
	PostDetailView, 
	#PostCreateView,
    postform,
	PostUpdateView,
	PostDeleteView,
    UserPostListView
)
from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='ecommerce-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #path('post/<int:pk>/', views.post_detail, name='post-detail'),
    #path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new/', postform, name='post-form'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='ecommerce-about'),
    path('commonuser/', views.commonuser, name='ecommerce-commonuser'),
]