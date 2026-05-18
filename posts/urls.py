from . import views
from django.urls import path
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('create/',views.post_create, name='create'),
    path('feed/',views.feed, name='feed'),
    path('like', views.like_post, name='like'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('api/posts/', api_views.post_list_api, name='api_posts'),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
]