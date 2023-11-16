from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_signup,name='login-signup'),
    path('login/',views.login_page,name="log-in"),
    path('signup/',views.signup_page,name="sign-up"),
    path('index/<int:auth_id>',views.blog_index,name="blog-index"),
    path('category/<category>',views.blog_category,name="blog-category"),
    path('index/blog-details/<slug:slug>/<int:post_id>/<int:auth_id>',views.blog_detail,name="blog-details"),
    path('post/create/<int:auth_id>',views.create_post,name="blog-post"),
    path('post/<int:auth_id>/<int:post_id>/delete',views.blog_delete,name="post-delete"),
    path('post/<int:auth_id>/profile',views.show_profile,name="profile"),
]