from .models import Group, groupMember, Course
from users.models import User
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description', 'join_type', 'post_permission']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False},
            'join_type': {'required': True},
            'post_permission': {'required': True}
        }
