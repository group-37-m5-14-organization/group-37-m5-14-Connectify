from django.urls import path
from . import views
from likes.views import LikeView
from comments.views import CommentView, CommentDetailView

urlpatterns = [
    path("posts/", views.PostView.as_view()),
    path("posts/<int:pk>/", views.PostDetailsView.as_view()),
    path("posts/<int:pk>/like/", LikeView.as_view()),
    path("posts/<int:pk>/comment/", CommentView.as_view()),
    path("posts/<int:pk>/comment/<int:comment_id>/", CommentDetailView.as_view()),
]
