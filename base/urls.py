from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path("profile/<str:userId>/", views.userProfile, name="user-profile"),
    path("room/<str:roomId>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:roomId>", views.updateRoom, name="update-room"),
    path(
        "edit-message/<str:roomId>/<str:messageId>",
        views.updateMessage,
        name="edit-message",
    ),
    path("delete-room/<str:roomId>", views.deleteRoom, name="delete-room"),
    path(
        "delete-message/<str:roomId>/<str:messageId>",
        views.deleteMessage,
        name="delete-message",
    ),
    path("update-user/", views.updateUser, name="update-user"),
    path("topics/", views.topics, name="topics"),
    path("activity/", views.activities, name="activity"),
]
