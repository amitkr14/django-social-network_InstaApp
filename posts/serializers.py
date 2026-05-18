from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # We add custom fields to grab the username and count the likes 
    # instead of just returning raw ID numbers
    username = serializers.CharField(source='user.username', read_only=True)
    likes_count = serializers.IntegerField(source='liked_by.count', read_only=True)

    class Meta:
        model = Post
        # These are the exact fields the API will expose to the public
        fields = ['id', 'username', 'title', 'caption', 'image', 'likes_count', 'created']