from django.shortcuts import render,redirect
from .forms import LoginForm,UserRegisterationForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Notification
from .forms import ProfileEditForm,UserEditForm
from posts.models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                # Redirect the user to the feed page here!
                return redirect('feed') 
            else:
                return HttpResponse('Invalid credentials')

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    profile = Profile.objects.filter(user=current_user).first()
    return render(request, 'users/index.html',{'posts':posts,'profile':profile})

def register(request):
    if request.method == 'POST':
        # Pass request.POST and request.FILES to capture text and image uploads
        user_form = UserRegisterationForm(request.POST)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user credentials
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            # Create the profile record linked to this user
            profile = Profile.objects.create(user=new_user)
            
            # If a registration photo was uploaded, attach it to the profile
            if profile_form.cleaned_data.get('photo'):
                profile.photo = profile_form.cleaned_data['photo']
                profile.save()
                
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegisterationForm()
        profile_form = ProfileEditForm()
        
    # Send both forms to your template context
    return render(request, 'users/register.html', {
        'user_form': user_form, 
        'profile_form': profile_form
    })       

@login_required
def edit(request):
    if request.method=='POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)   
    return render(request,'users/edit.html',{'user_form':user_form,'profile_form':profile_form})

@login_required
def public_profile(request, username):
    # Find the user by their username
    profile_user = get_object_or_404(User, username=username)
    
    # THE FIX: Safely get the profile, or automatically create a blank one if it's missing!
    profile, created = Profile.objects.get_or_create(user=profile_user)
    
    posts = Post.objects.filter(user=profile_user)
    
    # Check if the logged-in user is already following this profile
    is_following = False
    if request.user.profile.follows.filter(id=profile.id).exists():
        is_following = True
        
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following
    }
    return render(request, 'users/public_profile.html', context)

@login_required
def follow_user(request):
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        target_profile = get_object_or_404(Profile, id=profile_id)
        current_profile = request.user.profile
        
        # Toggle the follow status inside follow_user
        if current_profile.follows.filter(id=profile_id).exists():
            current_profile.follows.remove(target_profile)
            is_following = False
            # Remove the notification if they unfollow
            Notification.objects.filter(user=target_profile.user, sender=request.user, notification_type=3).delete()
        else:
            current_profile.follows.add(target_profile)
            is_following = True
            # Create a Follow notification
            Notification.objects.create(user=target_profile.user, sender=request.user, notification_type=3)
            
        return JsonResponse({
            'is_following': is_following, 
            'follower_count': target_profile.followed_by.count()
        })
    
@login_required
def search_users(request):
    # Get the search term from the URL parameter '?q=...'
    query = request.GET.get('q')
    results = []
    
    if query:
        # icontains makes the search case-insensitive 
        results = User.objects.filter(username__icontains=query)
        
    return render(request, 'users/search_results.html', {'results': results, 'query': query})    

@login_required
def notifications(request):
    # Fetch all notifications for the logged-in user, ordered by newest first
    user_notifications = Notification.objects.filter(user=request.user).order_by('-date')
    
    # Mark them all as seen the moment they open the page
    user_notifications.filter(is_seen=False).update(is_seen=True)
    
    return render(request, 'users/notifications.html', {'notifications': user_notifications})