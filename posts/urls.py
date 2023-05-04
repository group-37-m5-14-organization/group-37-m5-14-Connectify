from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostView.as_view()),
    path("posts/<int:pk>/", views.PostDetailsView.as_view()),
]
