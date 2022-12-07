from django.urls import path
from . import views

urlpatterns = [

    # Application Routes
    path("", views.index, name="index"),
    path("add_suite", views.add_suite, name="add_suite"),
    path("add_list", views.add_list, name="add_list"),
    path("add_to_list", views.add_to_list, name="add_to_list"),
    path("add_review/<int:suite_id>", views.add_review, name="add_review"),
    path("edit_review/<int:review_id>", views.edit_review, name="edit_review"),
    path("delete_list/<int:list_id>", views.delete_list, name="delete_list"),
    path("get_suite", views.get_suite, name="get_suite"),
    path("list/<int:list_id>", views.list, name="list"),
    path("suite/<int:suite_id>", views.suite, name="suite"),
    path("suite/<int:suite_id>/reviews", views.suite_reviews, name="suite_reviews"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/lists", views.lists, name="lists"),
    path("profile/<str:username>/reviews", views.user_reviews, name="user_reviews"),
    path("review/<int:review_id>", views.review, name="review"),

    # User Authentication
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

]