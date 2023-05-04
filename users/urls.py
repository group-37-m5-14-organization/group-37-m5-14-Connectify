from django.urls import path
from . import views
import friends.views as friends_views
from follows import views

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
    path("users/<int:pk>/follow/", views.FollowView.as_view()),
    path("users/<int:pk>/follow/", views.FollowDestroyView.as_view()),
    path("users/<int:pk>/follows/", views.FollowedListView.as_view()),
    path("users/<int:pk>/following/", views.FollowListView.as_view())
]
