from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, throttling
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.core.exceptions import ValidationError

from .serializers import UserRegistrationSerializer


# Helper function to generate JWT tokens
def get_tokens_for_user(user):
    """
    Generates JWT refresh and access tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Protect API with authentication and throttling
class ProtectedApiView(APIView):
    """
    API endpoint that requires authentication and applies rate limiting to users.
    """
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access this
    throttle_classes = [throttling.UserRateThrottle]  # Rate limiting per user

    def get(self, request):
        """
        Handles GET requests for the protected API.
        """
        return Response({"message": "This is a protected API!"})


# Login API with brute-force protection
class LoginView(APIView):
    """
    API endpoint for user authentication. Implements brute-force protection.
    """
    throttle_classes = [throttling.AnonRateThrottle]  # Limit login attempts for unauthenticated users

    def post(self, request):
        """
        Handles user login by verifying credentials and returning JWT tokens.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)


# Register API with password validation
@api_view(['POST'])
def register(request):
    """
    API endpoint for user registration. Ensures password validation before saving the user.
    """
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                validate_password(request.data['password'], user=user)  # Ensure strong passwords
            except ValidationError as e:
                user.delete()  # Prevent saving weak passwords
                return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Protected User Info API
class AccountInfoView(APIView):
    """
    API endpoint to retrieve user account information. Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns the username of the authenticated user.
        """
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)


# Logout API (blacklist refresh token)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    API endpoint for logging out users by blacklisting the refresh token.
    """
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# Secure Dashboard API
class DashboardView(APIView):
    """
    API endpoint to fetch dashboard data for authenticated users. Implements rate limiting.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]  # Limit request rate per user

    def get(self, request):
        """
        Returns a welcome message and user information for the dashboard.
        """
        dashboard_data = {
            "message": "Welcome to the Dashboard!",
            "user_info": {
                "username": request.user.username,
                "email": request.user.email
            }
        }
        return Response(dashboard_data)
