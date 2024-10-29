from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def validate_phone_number(self, value):
        phone_regex = r'^09\d{9}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError('phone number must be 11 digits')