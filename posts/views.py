from django.shortcuts import render, redirect
from .forms import PostCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import PostCreationForm, CommentForm, PostEditForm
from users.models import Notification,Profile

@login_required
def post_create(request):
    if request.method=='POST':
        form = PostCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('feed')
    else:
        form = PostCreationForm()
    return render(request,'posts/create.html',{'form':form})    


@login_required
def feed(request):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            
            # 1. Figure out which post they commented on
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            
            # 2. Attach the username since your posted_by is a CharField
            new_comment.posted_by = request.user.username 
            
            # 3. Save to the database and refresh the feed
            # 3. Save to the database
            new_comment.save()
            
            # NEW: Create a Comment notification
            if post.user != request.user:
                Notification.objects.create(
                    user=post.user, 
                    sender=request.user, 
                    post=post, 
                    notification_type=2, 
                    text_preview=new_comment.body[:50] # Save the first 50 chars of the comment
                )
                
            return redirect('feed')
    else:
        # For normal page loads, just create a blank form
        comment_form = CommentForm()
        
    posts = Post.objects.all()
    return render(request, 'posts/feed.html', {'posts': posts, 'comment_form': comment_form})


@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        # CORRECT Toggle the like status
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            is_liked = False
            # Remove notification if unliked
            Notification.objects.filter(user=post.user, sender=request.user, post=post, notification_type=1).delete()
        else:
            post.liked_by.add(request.user)
            is_liked = True
            # Create a Like notification (only if they aren't liking their own post!)
            if post.user != request.user:
                Notification.objects.create(user=post.user, sender=request.user, post=post, notification_type=1)
                
        # Get the username of the first liker
        first_liker = post.liked_by.first().username if post.liked_by.exists() else None
            
        # Send the count AND the first liker's name back to the browser
        return JsonResponse({
            'is_liked': is_liked, 
            'like_count': post.liked_by.count(),
            'first_liker': first_liker
        })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # SECURITY CHECK: Kick them out if they don't own the post!
    if post.user != request.user:
        return redirect('feed')
        
    if request.method == 'POST':
        # instance=post tells Django to update the existing post, not create a new one
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        # Pre-fill the form with the current title and caption
        form = PostEditForm(instance=post)
        
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # SECURITY CHECK: Only delete if the logged-in user owns it
    if request.method == 'POST' and post.user == request.user:
        post.delete()
        
    return redirect('feed')    