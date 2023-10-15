from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm,createBlog,CommentForm,PostForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


from .models import Post


# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at')
    posts.liker = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.author = request.user
                post_id = request.POST.get('post_id')  
                if post_id:
                    post =Post.objects.get(pk=post_id)
                    comment.post = post
                    comment.save()
                    form = CommentForm()
            else:
                return redirect('login') 
    else:
        form = CommentForm()
    return render(request, 'create/blogLists.html', {'posts': posts,'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)  
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def newBlog(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = createBlog(request.POST,request.FILES)
            if(form.is_valid()):
                post = form.save(commit=False)
                post.author=request.user
                if request.FILES.get('imagespost') is not None:
                    post.imagespost = request.FILES['imagespost']
                post.is_public = request.POST.get('is_public')
                post.liker = request.user
                post.save()
                return redirect('home')
    return render(request,'create/blog.html')

def myBlogs(request):
    post = Post.objects.filter(author=request.user)
    return render(request, 'create/myBlogs.html', {'post': post})

def deleteBlog(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('myBlogs')


def edit_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            if request.FILES.get('imagespost') is not None:
                form.imagespost = request.FILES['imagespost']
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'create/editBlog.html', {'form': form, 'post': post})

