from django.urls import path
from app_social import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.index,name='index'),
    path('profile', views.profile,name='profile'),
    path('message', views.message,name='message'),
    path('editProfile/<int:user_id>', views.editProfile,name='editProfile'),
    path('update_avatar/<int:user_id>', views.update_avatar,name='update_avatar'),
    path('profile/group', views.group,name='group'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('registe/', views.register,name='register'),
    path('login/', views.user_login,name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/allFriends', views.allFriends, name='All_friends'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('send_friend_request/<str:friend_username>/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests', views.friend_requests, name='friend_requests'),
    path('accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profileFriends'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('edit_Grouppost/<int:post_id>/', views.edit_Grouppost, name='edit_Grouppost'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('profile/allFollwers', views.allFollowers, name='All_followers'),
    path('user_profile/<int:user_id>/allFollwers', views.user_Followers, name='user_profileFollowers'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('like_Userpost/<int:post_id>/', views.like_Userpost, name='like_Userpost'),
    path('commentUserPost/<int:post_id>', views.comment_Userpost, name='commentUserPost'),
    path('search/', views.result_search, name='result_search'),
    path('comment/<int:post_id>', views.comment_post, name='commentPost'),
    path('delete_comment/<int:comment_id>', views.deleteComment, name='deleteComment'),
    path('group/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('profile/allFriends/unfriend/<int:friendship_id>/', views.unfriend, name='unfriend'),
    path('profile/allFriends/blocked/<int:friendship_id>/', views.block_friend, name='blocked'),
    path('profile/blockedFriends', views.blockingFriends, name='blockingFriends'),
    path('unblock/<int:friendship_id>/', views.unblock, name='unblock'),
    path('like_Grouppost/<int:post_id>/<int:group_id>/', views.like_Grouppost, name='like_Grouppost'),
    path('chat/<str:username>',views.chatPage,name='chat'),
    path('Mainchat',views.MainPageChat,name='Pagechat'),
    path('write_post', views.write_post, name='write_post'),
    path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),

]
