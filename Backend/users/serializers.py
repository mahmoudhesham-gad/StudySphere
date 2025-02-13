from django.contrib.auth.password_validation import validate_password
import email_validator
from rest_framework import serializers
from .models import User, Profile 
from django.contrib.auth import authenticate


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
            email_validator.validate_email(data['email'], check_deliverability=True) 
        except email_validator.EmailNotValidError as e:
            raise serializers.ValidationError({"email": str(e)})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        user_profile = Profile.objects.create(user=user)
        return user
    
class UserLoginSerializer(serializers.Serializer): 
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        # Authenticate the user using email and password
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email and password combination.")

        return user




    
        



