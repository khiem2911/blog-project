from django.shortcuts import render,redirect,get_object_or_404
from .forms import createGroup,GroupPostForm,CommentForm,ReplyCommentForm,CustomUserCreationForm,CustomAuthenticationForm,CustomPasswordChangeForm,PostForm
from .models import Group,GroupPost,Comment,CustomUser,FriendRequest,Friendship,Post,Image,Follow,CommentPost,ReplyCommentPost,Video,ChatModel
from django.contrib.auth import login,update_session_auth_hash
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect




def write_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['content'] or request.FILES.getlist('images') or  request.FILES.getlist('videos'):
                username = request.POST.get('otherUser-name')
                content = request.POST.get('content')
                other_user = get_object_or_404(CustomUser, username=username)
                post = Post(author=request.user,profile=other_user,content = content)
                post.save()
                if request.FILES.getlist('images'):
                    images = request.FILES.getlist('images')
                    for image in images:
                        new_image = Image(image=image)
                        new_image.save()
                        post.images.add(new_image)
                if request.FILES.getlist('videos'):
                        videos = request.FILES.getlist('videos')
                        for video in videos:
                            new_video = Video(video=video)
                            new_video.save()
                            post.video.add(new_video)
                return redirect('app_social:user_profile', username=username)
    else:
        return redirect('app_social:login')

def MainPageChat(request):
    if request.user.is_authenticated:
        userInfo = request.user
        users  = Friendship.objects.filter(user1=userInfo,blocked=False)
        new_array = [friendship.user2 for friendship in users]
        users = new_array
        return render(request, 'mainChat.html', context={'users': users})
    else:
        return redirect('app_social:login')


def chatPage(request, username):
        user_obj = CustomUser.objects.get(username=username)
        userInfo = request.user
        users  = Friendship.objects.filter(user1=userInfo,blocked=False)
        new_array = [friendship.user2 for friendship in users]
        users = new_array
        if request.user.id > user_obj.id:
            thread_name = f'chat_{request.user.id}-{user_obj.id}'
        else:
            thread_name = f'chat_{user_obj.id}-{request.user.id}'
        message_objs = ChatModel.objects.filter(thread_name=thread_name)
        return render(request, 'mainChat.html', context={'user': user_obj, 'users': users, 'messages': message_objs})



def index(request):
    posts = Post.objects.order_by('-created_at')
    comments = CommentPost.objects.order_by('-created_at')
    reply_comment_post = ReplyCommentPost.objects.order_by('-created_at')
    if(request.user):
     user = request.user
     for post_id in posts.all():
            post = posts.get(id=post_id.id)
            if user in post.likes.all():
                post.liked = True
            else:
                post.liked = False
            post.save()
     if not isinstance(user, AnonymousUser):
         user_groups = user.groups_joined.all()
         user = request.user
         all_groups = Group.objects.exclude(members=user)
         suggested_friends = CustomUser.objects.exclude(id=user.id)
         sent_friend_requests = FriendRequest.objects.filter(from_user=user, is_accepted=False).values_list('to_user', flat=True)
         suggested_friends = suggested_friends.exclude(id__in=sent_friend_requests)
         user_friends = Friendship.objects.filter(user1=user).values_list('user2', flat=True)
         suggested_friends = suggested_friends.exclude(id__in=user_friends)
         context = {
         'user':user,
         'suggested_friends': suggested_friends,
         'user_groups': user_groups,
         'all_groups': all_groups,
         'posts': posts,
         'comments': comments,
         'reply_comment_post': reply_comment_post,
         
         }
         return render(request, 'index.html', context)
    return render(request,"index.html",{'posts': posts})

def user_profile_view(request,username):
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.get(username=username) 
        is_blocked_by_current_user = Friendship.objects.filter(user1=request.user, user2=custom_user, blocked=True).exists()
        if(is_blocked_by_current_user):
         return redirect(reverse('app_social:blockingFriends') + '?show_alert=true')
        is_blocked_by_user =  Friendship.objects.filter(user1=custom_user, user2=request.user, blocked=True).exists()
        if is_blocked_by_user:
         return redirect(reverse('app_social:index') + '?blocked=true')
        following_users = request.user.following.all()
        is_following = following_users.filter(following__id=custom_user.id).exists()
        request.session['is_following'] = is_following
        if(custom_user==request.user):
            return redirect('app_social:profile')
        posts = Post.objects.filter(author=custom_user,profile__isnull=True).union(Post.objects.filter(profile=custom_user)).order_by('-created_at')
        for post in posts.all():
            if request.user in post.likes.all():
                post.liked = True
            else:
                post.liked = False
            post.save()
        comments = CommentPost.objects.order_by('-created_at')
        user = request.user
        reply_comment_post = ReplyCommentPost.objects.order_by('-created_at')
        custom_user.is_friend = user.is_friend_with(custom_user)
        context = {
            'profile_user': custom_user,
            'posts': posts,
            'comments': comments,
            'reply_comment_post': reply_comment_post
        }
        return render(request, 'user/user_profile.html', context)
    else:
        return redirect('app_social:login')

def leave_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    
    if request.method == 'POST':
        if group.leave_group(request.user):
            return redirect('app_social:index')
        
def unfriend(request, friendship_id):
    if request.method == 'POST':
        current_user_id = request.user.id
        friendship = Friendship.objects.filter(
            user1_id=current_user_id, user2_id=friendship_id
        ).first()
        friendship.unfriend()
        userInfo = request.user
        friends = Friendship.objects.filter(user1=userInfo)
        context = {
        'friends': friends
        }
        return render(request,"friends/friend.html",context)
    
   
def block_friend(request, friendship_id):
    current_user_id = request.user.id
    if request.method == 'POST':
        friendship = Friendship.objects.filter(
            user1_id=current_user_id, user2_id=friendship_id
         ).first()
        friendship.block()
        userInfo = request.user
        friends = Friendship.objects.filter(user1=userInfo,blocked=False)
        context = {
        'friends': friends
        }
        return render(request,"friends/friend.html",context)
    
def unblock(request, friendship_id):
    current_user_id = request.user.id
    if request.method == 'POST':
        friendship = Friendship.objects.filter(
            user1_id=current_user_id, user2_id=friendship_id
         ).first()
        friendship.unblock()
        return redirect('app_social:blockingFriends') 


def user_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    friends = Friendship.objects.filter(user1=user)
    context = {
        'userInfos': user,
        'friends': friends,
    }
    return render(request, 'user/user_friends.html', context)

def blockingFriends(request):
    blocked_friends_list = request.user.blocked_friends()
    print(blocked_friends_list)
    return render(request, 'blocked/blockedFriends.html', {'blocked_friends': blocked_friends_list})



def allFriends(request):
    userInfo = request.user
    friends = Friendship.objects.filter(user1=userInfo,blocked=False)
    context = {
        'friends': friends
    }
    return render(request,"friends/friend.html",context)

def user_Followers(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    following = user.following.all()
    context = {
        'userInfos': user,
        'followers':following
    }
    return render(request,"user/user_followers.html",context)
def allFollowers(request):
    user = request.user

    following = user.following.all()
    context = {
        'followers':following
    }
    return render(request,"followers/followers.html",context)
def profile(request):
    user_groups = Group.objects.filter(members=request.user)
    comments = CommentPost.objects.order_by('-created_at')
    reply_comment_post = ReplyCommentPost.objects.order_by('-created_at')
    userInfo = request.user
    posts = Post.objects.filter(author=userInfo,profile__isnull=True).union(Post.objects.filter(profile=userInfo)).order_by('-created_at')
    for post in posts:
        if userInfo in post.likes.all():
            post.liked = True
        else:
            post.liked = False
        post.save() 
    
    context = {
         'user_groups': user_groups,
         'posts': posts,
         'userInfo': userInfo,
         'comments': comments,
         'reply_comment_post': reply_comment_post,

         }
    return render(request,"profile.html", context)
def message(request):
    return render(request,"message.html")

def editProfile(request,user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.date_of_birth = request.POST['date_of_birth']
        user.lives = request.POST['lives']
        user.email = request.POST['email']
        user.bio = request.POST['bio']
        user.website = request.POST['website']
        user.gender = request.POST['gender']
        if request.FILES.get('avatar') is not None:
            user.avatar = request.FILES['avatar'] 
        user.save()
        return redirect('app_social:profile')
    return render(request,"editProfile.html",{'user': user})

def update_avatar(request,user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.FILES.get('avatar'):
        user.avatar = request.FILES['avatar'] 
        user.save()
        return redirect('app_social:editProfile',user_id=user_id)
    elif request.FILES.get('imgcover'):
        user.imgcover = request.FILES['imgcover'] 
        user.save()
        return redirect('app_social:editProfile',user_id=user_id)
    return redirect('app_social:editProfile',user_id=user_id)


def like_Grouppost(request, post_id,group_id):
    if request.user.is_authenticated: 
        post = get_object_or_404(GroupPost, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            
        post.save()

        return redirect('app_social:group_detail',group_id=group_id)
    

def like_post(request, post_id):
    if request.user.is_authenticated: 
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            
        post.save()

        like_post_in_profile = request.GET.get('like_post_in_profile', None)
        if like_post_in_profile == 'true':
            return redirect('app_social:profile')

        return redirect('app_social:index')
    else:
        return redirect('app_social:login')

def like_Userpost(request, post_id):
    if request.user.is_authenticated: 
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            
        post.save()

       
        username = request.GET.get('username')
        

        return redirect('app_social:user_profile',username=username)
    else:
        return redirect('app_social:login')

def group(request):
    if(request.method == 'POST'):
        form = createGroup(request.POST,request.FILES)
        if(form.is_valid()):
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            group.members.add(request.user)
            return redirect('app_social:profile')
    else:
        return render(request,"group/group.html")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
                user.save()
            else:
                user.avatar = 'avatar/avatar2.png'
                user.save()
            login(request, user)
            return redirect('app_social:index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('app_social:index') 
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('app_social:index') 
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'registration/change_password.html', {'form': form})


def join_group(request, group_id):
    user = request.user
    group = Group.objects.get(pk=group_id)
    group.members.add(user)
    return redirect('app_social:index')
 

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_posts = GroupPost.objects.filter(group=group).order_by('-created_at')
    group_members = group.members.all()
    comment_form = CommentForm()
    reply_form = ReplyCommentForm()
    user_joined_group = group.members.filter(id=request.user.id).exists()
    user = request.user
   
    for member in group_members:
        member.is_friend = user.is_friend_with(member)
        print(f"{user.username} is friend with {member.username}: {member.is_friend}")


    for post in group_posts.all():
            if user in post.likes.all():
                post.liked = True
            else:
                post.liked = False
            post.save()
    if request.method == 'POST':
        if 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                post_id = request.POST.get('post_id')  
                current_post = get_object_or_404(group_posts, id=post_id)  
                comment = comment_form.save(commit=False)
                comment.group = group
                comment.post = current_post
                comment.author = request.user
                comment.save()
        elif 'reply_comment' in request.POST:
            reply_form = ReplyCommentForm(request.POST)
            if reply_form.is_valid():
                cmt_id = request.POST.get('comment_id')  
                comment = Comment.objects.get(id=cmt_id)
                reply_comment = reply_form.save(commit=False)
                reply_comment.group = group
                reply_comment.author = request.user
                reply_comment.comment = comment
                reply_comment.save()
        elif 'delete_post' in request.POST:
            post_id = request.POST.get('post_id')  
            post = GroupPost.objects.get(id=post_id)
            if post.author == request.user:
                post.delete()
        else:
            form = GroupPostForm(request.POST)
            if user_joined_group:
                if form.is_valid():
                    post = form.save(commit=False)
                    post.group = group
                    post.author = request.user
                    post.save()
                    if request.FILES.getlist('images'):
                        images = request.FILES.getlist('images')
                        for image in images:
                                new_image = Image(image=image)
                                new_image.save()
                                post.images.add(new_image)
                    if request.FILES.getlist('videos'):
                        videos = request.FILES.getlist('videos')
                        for video in videos:
                                new_video = Video(video=video)
                                new_video.save()
                                post.video.add(new_video)
                    return redirect('app_social:group_detail', group_id=group_id)
            else:
                return redirect(reverse('app_social:index') + '?show_alertGroup=true')      
    context = {
        'group': group,
        'group_posts': group_posts,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'group_members': group_members,
        'user_joined_group':  user_joined_group 
    }
    return render(request, 'group/group_detail.html', context)

def delete_group(request,group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':        
        group.delete()
        return redirect(reverse('app_social:profile') + '?show_alertDelete=true')      

@login_required
def send_friend_request(request, friend_username):
    if request.user.is_authenticated:
        try:
            friend = CustomUser.objects.get(username=friend_username)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Người bạn không tồn tại.')
            return redirect('app_social:index')  

        existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=friend, is_accepted=False,rejected=False)
        if existing_request.exists():
            messages.warning(request, 'Bạn đã gửi lời mời kết bạn tới người này.')
            return redirect('app_social:index')  
        else:
            friend_request = FriendRequest(from_user=request.user, to_user=friend)
            friend_request.save()
            group_id = request.GET.get('group_id')
            if group_id:
             return redirect('app_social:group_detail',group_id=group_id)
            else :
             return redirect('app_social:index')  
    else:
        messages.error(request, 'Bạn cần đăng nhập để gửi lời mời kết bạn.')
        return redirect('login')  


@login_required
def accept_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)

   
    friend_request.is_accepted = True
    friend_request.save()

    
    Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
    Friendship.objects.create(user1=friend_request.to_user, user2=friend_request.from_user)
    return redirect('app_social:friend_requests')
    

@login_required
def reject_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
    friend_request.rejected = True
    friend_request.save()
    return redirect('app_social:friend_requests')

@login_required
def friend_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False,rejected=False)
    return render(request, 'user/friend_request.html', {'received_requests': received_requests})



def create_post(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['content'] or request.FILES.getlist('images') or  request.FILES.getlist('videos'):
                author = request.user
                content = request.POST['content']
                
                post = Post(author=author, content=content)
                post.save()
                if request.FILES.getlist('images'):
                    images = request.FILES.getlist('images')
                    for image in images:
                        new_image = Image(image=image)
                        new_image.save()
                        post.images.add(new_image)
                if request.FILES.getlist('videos'):
                    videos = request.FILES.getlist('videos')
                    for video in videos:
                        new_video = Video(video=video)
                        new_video.save()
                        post.video.add(new_video)
            else:
                messages.error(request, "Cần có hình, video hoặc nội dung bài viết!")
        
        if request.POST.get('return-profile'):
            return HttpResponseRedirect(reverse('app_social:profile'))
        return HttpResponseRedirect(reverse('app_social:index'))
    else:
        return redirect('app_social:login')
    
def delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    username = request.GET.get('username')
    if username:
        return redirect('app_social:user_profile',username=username)
    else:
        return redirect('app_social:profile')

def edit_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    image = request.FILES.getlist('images')
    print(request.POST)
    print(image)
    if request.method == 'POST':
        if request.POST['content'] or request.FILES.getlist('images') or request.FILES.getlist('videos'):
                post.content = request.POST['content']
                
                if request.FILES.getlist('images'):
                    images = request.FILES.getlist('images')
                    for old_image in post.images.all():
                        old_image.delete()
                    for image in images:
                        new_image = Image(image=image)  
                        new_image.save()
                        post.images.add(new_image)
                
                elif request.FILES.getlist('videos'):
                    videos = request.FILES.getlist('videos')
                    print(videos)
                    for old_video in post.video.all():
                        old_video.delete()
                    for video in videos:
                        new_video = Video(video=video)  
                        new_video.save() 
                        post.video.add(new_video)
                post.save()
                return redirect('app_social:profile')
        else:
         return redirect('app_social:profile')
    else:
        return redirect('app_social:profile')
    



def edit_Grouppost(request,post_id):
    post = get_object_or_404(GroupPost, id=post_id)
    group_id = request.POST.get('group_id')
    images = request.FILES.getlist('images')
    if request.method == 'POST':
        if request.POST['content'] or request.FILES.getlist('images'):
                post.content = request.POST['content']
                if request.FILES.getlist('images'):
                    images = request.FILES.getlist('images')
                    for old_image in post.images.all():
                        old_image.delete()
                    for image in images:
                        new_image = Image(image=image)  
                        new_image.save()
                        post.images.add(new_image)
                
                elif request.FILES.getlist('videos'):
                    videos = request.FILES.getlist('videos')
                    for old_video in post.video.all():
                        old_video.delete()
                    for video in videos:
                        new_video = Video(video=video)  
                        new_video.save() 
                        post.video.add(new_video)
                post.save()
                return redirect('app_social:group_detail', group_id=group_id)
        else:
         return redirect('app_social:group_detail', group_id=group_id)
    

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    current_user = request.user
    
    if user_to_follow == current_user:
        return redirect('app_social:user_profile', username=user_to_follow.username)
    try:
        follow_relationship = Follow.objects.get(follower=current_user, following=user_to_follow)
        follow_relationship.delete()
        following_users = current_user.following.all()
        is_following = following_users.filter(following__id=user_to_follow.id).exists()
        request.session['is_following'] =  is_following 
    except Follow.DoesNotExist:
        Follow.objects.create(follower=current_user, following=user_to_follow)
        following_users = current_user.following.all()
        is_following = following_users.filter(following__id=user_to_follow.id).exists()
        request.session['is_following'] = is_following
    
    return redirect('app_social:user_profile', username=user_to_follow.username)

def result_search(request):
    value = request.GET.get("value_search")
    print(value)
    user = request.user
    all_groups = Group.objects.exclude(members=user)
    posts = Post.objects.filter(content__contains=value).order_by("-created_at")
    comments = CommentPost.objects.order_by('-created_at')
    reply_comment_post = ReplyCommentPost.objects.order_by('-created_at')
    suggested_friends = CustomUser.objects.exclude(id=user.id)
    sent_friend_requests = FriendRequest.objects.filter(from_user=user, is_accepted=False).values_list('to_user', flat=True)
    suggested_friends = suggested_friends.exclude(id__in=sent_friend_requests)
    user_friends = Friendship.objects.filter(user1=user).values_list('user2', flat=True)
    suggested_friends = suggested_friends.exclude(id__in=user_friends)
    context={
        'posts': posts,
        'comments': comments,
        'reply_comment_post': reply_comment_post,
        'all_groups' :  all_groups,
        'suggested_friends' :  suggested_friends
    }
    
    return render(request, "search.html",context )

def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        print(request.POST)
        if 'add_comment' in request.POST:
            author = request.user
            content = request.POST['content']
            commentPost = CommentPost(post=post,author=author, content=content)
            commentPost.save()
        elif 'reply_comment' in request.POST:
            cmt_id = request.POST['comment_id'] 
            comment = CommentPost.objects.get(id=cmt_id)
            author = request.user 
            text = request.POST['text']
            reply_comment_post = ReplyCommentPost(author=author,comment=comment,text=text)
            reply_comment_post.save()
        elif 'edit_comment' in request.POST:
            cmt_id = request.POST['comment_id'] 
            comment = CommentPost.objects.get(id=cmt_id)
            comment.content = request.POST['content']
            comment.save()
        if request.POST.get('return_profile'):
            return redirect('app_social:profile')
    return redirect('app_social:index')
            

def deleteComment(request, comment_id):
    comment = CommentPost.objects.get(id=comment_id)
    comment.delete()
    username = request.GET.get('username')
    if username:
        return redirect('app_social:user_profile',username=username)
    elif request.GET.get('return-p'):
        return redirect('app_social:profile')
    else:
        return redirect('app_social:index')


def comment_Userpost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    username = request.POST['username']
    if request.method == 'POST':
        if 'add_comment' in request.POST:
            author = request.user
            content = request.POST['content']
            commentPost = CommentPost(post=post,author=author, content=content)
            commentPost.save()
        elif 'reply_comment' in request.POST:
            cmt_id = request.POST['comment_id'] 
            comment = CommentPost.objects.get(id=cmt_id)
            author = request.user
            text = request.POST['text']
            reply_comment_post = ReplyCommentPost(author=author,comment=comment,text=text)
            reply_comment_post.save()
    return redirect('app_social:user_profile', username=username)