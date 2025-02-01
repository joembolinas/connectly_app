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

            # Check if required fields are present
            if 'username' not in data or 'email' not in data:
                return JsonResponse({'message': 'Username and email are required'}, status=400)

            # Check if username or email already exists
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({'message': 'Username already exists'}, status=500)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'Email already exists'}, status=500)

            # Create user
            user = User.objects.create(username=data['username'], email=data['email'])
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

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

            # Check if required fields are present
            if 'author' not in data or 'content' not in data:
                return JsonResponse({'message': 'Author ID and content are required'}, status=400)

            # Check if content is empty
            if not data['content'].strip():
                return JsonResponse({'message': 'Content cannot be empty'}, status=400)

            # Validate author existence
            try:
                author = User.objects.get(id=data['author'])
            except User.DoesNotExist:
                return JsonResponse({'message': 'Author not found'}, status=404)

            # Create post
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)