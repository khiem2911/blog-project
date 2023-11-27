from django.contrib import admin
from .models import Post, CustomUser,Comment,Group,Friendship,GroupPost,ReplyComment,FriendRequest,Image,Video,Follow,CommentPost,ReplyCommentPost,Fanpage,Post_Fanpage,ImagePostFanpage,VideoPostFanpage,CommentPostFanpage,ReplyCommentPostFanpage

# Register your models here.
admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Friendship)
admin.site.register(GroupPost)
admin.site.register(ReplyComment)   
admin.site.register(FriendRequest)
admin.site.register(Image)
admin.site.register(Follow)
admin.site.register(CommentPost)
admin.site.register(ReplyCommentPost)
admin.site.register(Video)
admin.site.register(Fanpage)
admin.site.register(Post_Fanpage)
admin.site.register(ImagePostFanpage)
admin.site.register(VideoPostFanpage)
admin.site.register(CommentPostFanpage)
admin.site.register(ReplyCommentPostFanpage)




