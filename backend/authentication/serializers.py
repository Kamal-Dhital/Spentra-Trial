# Python
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles the creation of a new user with a fullname, email, and password.
    """

    fullname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        """
        Meta-class to specify the model and fields to include in the serializer.
        """
        model = User
        fields = ('fullname', 'email', 'password')

    def create(self, validated_data):
        """
        Create a new user instance with the provided validated data.

        Args:
            validated_data (dict): The validated data containing the fullname, email, and password.

        Returns:
            User: The created user instance.
        """
        email = validated_data['email']
        password = validated_data['password']
        fullname = validated_data['fullname']
        # Use email as username and store fullname in first_name (adjust as needed)
        user = User.objects.create_user(username=email, email=email, password=password, first_name=fullname)
        return user


class LoginSerializer(serializers.Serializer):
    """
        Serializer for user login.
    Validates user credentials (email and password) and authenticates the user.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the provided email and password.

        Args:
            data (dict): The data containing email and password.

        Returns:
            dict: The validated data with the authenticated user is added.

        Raises:
            serializers.ValidationError: If the credentials are invalid.
        """
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        data['user'] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value