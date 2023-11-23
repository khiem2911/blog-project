from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

# Create your models here.

class CustomUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True, default=None)
    online_status = models.BooleanField(default=False)
    GENDER_CHOICES = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
    )
    gender = models.CharField(
        max_length=3, choices=GENDER_CHOICES, blank=True, null=True, default=None)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    imgcover = models.ImageField(upload_to='imgcover/', blank=True, null=True)
    website = models.TextField(
        max_length=255, default='https://khiem2911.pythonanywhere.com/')
    lives = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.username

    def is_friend_with(self, user):
        return Friendship.objects.filter(
            (Q(user1=self, user2=user) | Q(user1=user, user2=self)) &
            Q(blocked=False)
        ).exists()

    def blocked_friends(self):
        blocked_by_self_ids = Friendship.objects.filter(
            blocked=True,
            user1=self
        ).values('user2')
        blocked_by_self = CustomUser.objects.filter(id__in=blocked_by_self_ids)
        return blocked_by_self


class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message
    
class ChatNotification(models.Model):
    chat = models.ForeignKey(to=ChatModel, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class Video(models.Model):
    video = models.FileField(upload_to='videos/', blank=True, null=True)

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    images = models.ManyToManyField(Image, blank=True)
    video = models.ManyToManyField(Video, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.ManyToManyField(
    CustomUser, related_name='liked_posts', blank=True)
    liked = models.TextField(default=False)
    profile = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts',null=True)

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} thích bài viết của {self.post.author.username}"


class Friendship(models.Model):
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friends')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user1.username} và {self.user2.username} là bạn"

    def unfriend(self):
        Friendship.objects.filter(Q(user1=self.user1, user2=self.user2) | Q(user1=self.user2, user2=self.user1)).delete()

    

    def block(self):
        self.blocked = True
        self.save()

    def unblock(self):
        self.blocked = False
        self.save()


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(
        CustomUser, related_name='groups_joined', blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='groups_created')
    created_at = models.DateTimeField(auto_now_add=True)
    group_picture = models.ImageField(upload_to='group_pics/', blank=True)

    def __str__(self):
        return self.name

    def leave_group(self, user):
        if user in self.members.all():
            self.members.remove(user)
            return True
        return False


class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    images = models.ManyToManyField(Image, blank=True)
    video = models.ManyToManyField(Video, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
    CustomUser, related_name='liked_Groupposts', blank=True)
    liked = models.TextField(default=False)
    def __str__(self):
        return f"Post by {self.author.username} in {self.group}"


class Comment(models.Model):
    post = models.ForeignKey(
        GroupPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class ReplyComment(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ['follower', 'following']


class CommentPost(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='commentsPost')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class ReplyCommentPost(models.Model):
    comment = models.ForeignKey(
        CommentPost, on_delete=models.CASCADE, related_name='repliesPost')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment}"
