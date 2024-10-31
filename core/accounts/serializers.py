from rest_framework import serializers
from .models import User
import re
import string


def clean_name(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin cant be use')
    return value


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [clean_name,]},
            'first_name': {'validators': [clean_name]},
            'last_name': {'validators': [clean_name]},
        }

    def validate_phone_number(self, value):
        phone_regex = r'^09\d{9}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError('phone number invalid')
        return value

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def validate_age(self, value):
        if value < 12:
            raise serializers.ValidationError("Age must be greater than or equal to 12")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')
        if not any(char in string.ascii_uppercase for char in value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter')
        if not any(char in string.ascii_lowercase for char in value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter')
        if not any(char in string.digits for char in value):
            raise serializers.ValidationError(' Password must contain at least one number')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        del validated_data['confirm_password']
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user