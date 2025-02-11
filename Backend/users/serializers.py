from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Profile 


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
        'email': {'required': True},
        'username': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
          raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        try:
            validate_email(data['email'])  # Use Django's built-in email validator
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user_profile = Profile.objects.create(user=user)
        return user
    



    
        



