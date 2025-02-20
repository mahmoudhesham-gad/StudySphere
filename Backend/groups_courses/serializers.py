from .models import Group, GroupMember, JoinRequest, Course
from users.models import User
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'owner', 'name', 'description', 'join_type', 'post_permission', 'edit_permissions', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = GroupMember
        fields = ['user', 'user_role', 'joined_at']
        read_only_fields = ['joined_at']

class CreateGroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['user']

class GroupJoinRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = JoinRequest
        fields = ['user', 'created_at']
        read_only_fields = ['created_at']

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description']

class CourseSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta:
        model = Course
        fields = ['id', 'group', 'name', 'description']
        read_only_fields = ['id', 'group']

