from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import (
    RegisterSerializer, LoginSerializer
)

from rest_framework_simplejwt.tokens import RefreshToken

OTP_STORAGE = {}

def get_tokens_for_user(user):
    """
    Generate JWT tokens (refresh and access) for the given user.

    Args:
        user (User): The user instance for which tokens are generated.

    Returns:
        dict: A dictionary containing the refresh and access tokens as strings.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    """
    API view for user registration.

    Methods:
        post(request): Handles user registration and returns JWT tokens upon success.
    """
    def post(self, request):
        """
        Handle POST requests for user registration.

        Args:
            request (Request): The HTTP request object containing user data.

        Returns:
            Response: A response object with a status code and either the generated tokens
                      or validation errors.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            login(request, user)
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)