from django.urls import path
from . import views
import friends.views as friends_views
from follows import views as follows_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/login/", views.LoginView.as_view()),
    path(
        "users/<int:pk>/friends/",
        friends_views.CreateDestroyFriendRequestView.as_view(),
    ),
    path(
        "users/friends/requests/",
        friends_views.ListFriendRequestView.as_view(),
    ),
    path("users/friends/", friends_views.ListFriendView.as_view()),
    path("users/<int:pk>/follow/", follows_views.FollowView.as_view()),
    path("users/follows/", follows_views.FollowedListView.as_view()),
    path("users/following/", follows_views.FollowListView.as_view()),
]
