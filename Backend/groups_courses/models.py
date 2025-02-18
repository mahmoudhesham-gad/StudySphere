from django.db import models
from users.models import User
import uuid

# Create your models here.

class Group(models.Model):
    # Join types for the group
    JOIN_CHOICES = [
        ('open', 'Open - anyone can join'),
        ('request', 'Request Approval - joining requires admin approval'),
        ('invite', 'Invite Only - only invited users can join'),
    ]
    
    # Posting permissions for the group
    POST_CHOICES = [
        ('members', 'Members Only - only group members can post'),
        ('moderators', 'Moderators Only - only moderators (or admins) can post'),
        ('admins', 'Admins Only - only admins can post'),
        ('owner', 'Owner Only - only the owner can post'),
    ]

    MEMBERS_EDIT_PERMISSIONS = [
        ('moderators', 'Moderators and above can edit members'),
        ('admins', 'Only admins and owner can edit members'),
        ('owner', 'Only owner can edit members'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    join_type = models.CharField(
        max_length=20,
        choices=JOIN_CHOICES,
        default='open'
    )

    post_permission = models.CharField(
        max_length=20,
        choices=POST_CHOICES,
        default='members'
    )

    edit_permissions = models.CharField(
        max_length=20,
        choices=MEMBERS_EDIT_PERMISSIONS,
        default='admins'
    ) 

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.user_role}"
    

class JoinRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} requested to join {self.group.name}"


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('group', 'name')


    def __str__(self):
        return self.name
    
