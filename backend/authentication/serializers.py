# Python
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('fullname', 'email', 'password')

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        fullname = validated_data['fullname']
        # Use email as username and store fullname in first_name (adjust as needed)
        user = User.objects.create_user(username=email, email=email, password=password, first_name=fullname)
        return user