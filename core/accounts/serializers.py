from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone_number(self, value):
        phone_regex = r'^09\d{9}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError('phone number invalid')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user