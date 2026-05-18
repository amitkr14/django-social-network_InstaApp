from .models import Post, Comment
from django import forms

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =('title','image','caption')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # IMPORTANT: If your comment text field in models.py is named something 
        # else (like 'text' or 'content'), change 'body' to match it perfectly!
        fields = ('body',) 
        
        # Optional: Add Tailwind classes directly to the input to make it look clean
        widgets = {
            'body': forms.TextInput(attrs={
                'class': 'w-full border-none focus:ring-0 text-sm py-2 outline-none',
                'placeholder': 'Add a comment...'
            })
        }

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'caption')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'caption': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 3}),
        }        