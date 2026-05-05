from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .services import register_user, login_user, logout_user
from .utils import success_response, error_response

class RegisterView(APIView):
    def post(self, request):
        tokens, error = register_user(request.data)
        if error:
            return error_response(error)
        return success_response(tokens)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        tokens, error = login_user(username, password)
        if error:
            return error_response(error, 401)
        return success_response(tokens)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        success, error = logout_user(request.data.get('refresh'))
        if error:
            return error_response(error)
        return success_response({'message': 'Déconnexion réussie'})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return success_response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })