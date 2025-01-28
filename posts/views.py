from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from .models import User, Post

# Retrieve all users
def get_users(request):
    users = list(User.objects.values())
    return JsonResponse(users, safe=False)

# Create a user
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create(username=data['username'], email=data['email'])
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Retrieve all posts
def get_posts(request):
    posts = list(Post.objects.values())
    return JsonResponse(posts, safe=False)

# Create a post
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
