from django.urls import path
from myBlogs import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index,name='home'),
    path('login',views.user_login,name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('register/', views.register, name='register'),
    path('blog/', views.newBlog, name='blog'),
    path('myBlogs/', views.myBlogs, name='myBlogs'),
    path('post/<int:pk>/delete/', views.deleteBlog, name='delete_post'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),

]