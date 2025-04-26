# Python: backend/profiles/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'birth_date', 'profile_picture', 'phone_number', 'website']