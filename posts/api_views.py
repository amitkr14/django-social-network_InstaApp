from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def post_list_api(request):
    
    posts = Post.objects.all().order_by('-created')
    serializer = PostSerializer(posts, many=True)
    
    return Response(serializer.data)