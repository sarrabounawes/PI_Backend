from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
        'refresh': str(refresh),
    }

def register_user(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if User.objects.filter(username=username).exists():
        return None, 'Username déjà utilisé'
    user = User.objects.create_user(username=username, email=email, password=password)
    return generate_tokens(user), None

def login_user(username, password):
    user = authenticate(username=username, password=password)
    if not user:
        return None, 'Identifiants incorrects'
    return generate_tokens(user), None

def logout_user(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True, None
    except Exception:
        return False, 'Token invalide'