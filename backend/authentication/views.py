import random

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import (
    RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, VerifyOTPSerializer, SetNewPasswordSerializer
)
from django.contrib.auth.hashers import make_password
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
            """
            API view for user login.

            Methods:
                post(request): Authenticates the user and returns JWT tokens upon success.
            """
            def post(self, request):
                """
                Handle POST requests for user login.

                Args:
                    request (Request): The HTTP request object containing login credentials.

                Returns:
                    Response: A response object with JWT tokens if authentication is successful,
                              or validation errors if authentication fails.
                """
                serializer = LoginSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.validated_data['user']
                    login(request, user)
                    tokens = get_tokens_for_user(user)
                    return Response(tokens, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_otp():
    """
    Generate a 6-digit OTP.

    Returns:
        str: A randomly generated 6-digit OTP as a string.
    """
    return str(random.randint(100000, 999999))


class ForgotPasswordView(APIView):
    """
    API view for handling forgotten passwords.

    Methods:
        post(request): Accepts an email, generates an OTP, and sends it to the user.
    """
    def post(self, request):
        """
        Handle POST requests for generating an OTP.

        Args:
            request (Request): The HTTP request object containing the user's email.

        Returns:
            Response: A response object with a success message and the generated OTP,
                      or validation errors if the request is invalid.
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = generate_otp()
            OTP_STORAGE[email] = otp
            # For real applications, send the OTP via email instead of returning it.
            return Response({"message": "OTP generated.", "otp": otp}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
    API view for verifying OTPs.

    Methods:
        post(request): Verifies the OTP provided by the user.
    """
    def post(self, request):
        """
        Handle POST requests for OTP verification.

        Args:
            request (Request): The HTTP request object containing the email and OTP.

        Returns:
            Response: A response object with a success message if the OTP is valid,
                      or an error message if the OTP is invalid.
        """
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            stored_otp = OTP_STORAGE.get(email)
            if stored_otp == otp:
                return Response({"message": "OTP verified."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    """
    API view for setting a new password after OTP verification.

    Methods:
        post(request): Sets a new password for the user after verifying the OTP.
    """
    def post(self, request):
        """
        Handle POST requests for setting a new password.

        Args:
            request (Request): The HTTP request object containing the email, OTP, and new password.

        Returns:
            Response: A response object with a success message if the password is reset successfully,
                      or an error message if the OTP is invalid or the user does not exist.
        """
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            stored_otp = OTP_STORAGE.get(email)
            if stored_otp and stored_otp == otp:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
                user.password = make_password(new_password)
                user.save()
                del OTP_STORAGE[email]  # Invalidate OTP after use
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)