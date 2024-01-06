from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view(), name="index"), #{% url 'index' %}
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('forgot_password/',views.Forgot_password.as_view(),name="forgot_password"),
    path('change_password/<uidb64>/<token>/',views.MyPasswordResetConfirmView.as_view(),name="change_password"),
    path('password_reset_complete/',views.password_reset_complete,name="password_reset_complete"),
    path('add_new_blog/',views.UserBlogPostView.as_view(),name="add_new_blog"),
    path('comment-submit/', views.blog_comment, name="submit_comment"),
    path('blog_detail/<int:blog_id>/', views.BlogDetailView.as_view(), name="blog_detail"),
    path('profile/',views.UserProfile.as_view(),name="user_profile"),
    path('blog_update/<int:id>/',views.BlogUpdate.as_view(),name="blog_update"),
    path('blog_delete/<int:id>/',views.BlogDelete.as_view(),name="blog_delete"),
    path('search/', views.SearchView.as_view(), name='search'),
    path('blog-share/',views.ShareBlog.as_view(), name="share_blog")
    # path('blog_search_query/',views.blog_search_query,name="blog_search_query")
   
]