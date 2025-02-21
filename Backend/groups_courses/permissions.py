from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import GroupMember

def ensure_group_owner(request, group, message="You are not the owner of this group"):
    """
    this function checks if the user is the owner of the group

    Args:
        request: the request object
        group: the group object

    Raises:
        PermissionDenied: If the user is not the owner of the group
    """
    if group.owner != request.user:
        raise PermissionDenied(
            detail=message,
            code=status.HTTP_403_FORBIDDEN,
        )
        

def can_edit_members(user, group):
    if group.owner == user:
        return True

    roles_needed = {
        'admins': {'admin'},
        'moderators': {'admin', 'moderator'}
    }.get(group.edit_permissions, set())

    for member in group.members.all():
        if member.user == user:
            print(user, member, roles_needed)  
            return member.user_role in roles_needed

    return False


    
def ensure_can_edit_members(user, group, message="User doesn't have the permission needed"):
    """
    This function checks if the given user has the necessary permissions to edit members
    in the specified group. If not, it raises a PermissionDenied exception.

    Args:
        user: The user object to check permissions for
        group: The group object to check against
        message (str, optional): Custom error message. Defaults to "User doesn't have the permission needed"

    Raises:
        PermissionDenied: If the user lacks required permissions to edit group members

    """
    if not can_edit_members(user, group):
        raise PermissionDenied(
            detail=message,
            code=status.HTTP_403_FORBIDDEN,
        )
    
    
def check_group_admin(user, group):
    if group.owner == user:
        return True
    return GroupMember.objects.filter(user=user, group=group, role='admin').exists()


def has_higher_role(user, member):
    roles = ['admin', 'moderator', 'member']
    return roles.index(user.user_role) < roles.index(member.user_role)
    

def can_post(user, group):
    """
    Check if a user can post in a group based on post permissions

    Args:
        user: The user attempting to post
        group: The group where the post would be made

    Returns:
        bool: True if user can post, False otherwise
    """
    if user == group.owner:
        return True
    if group.post_permission == 'owner':
        return group.owner == user  

    roles_needed = {
        'members': {'member', 'moderator', 'admin'},
        'moderators': {'moderator', 'admin'},
        'admins': {'admin'}
    }.get(group.post_permission, set())

    member = group.members.filter(user=user).first()
    if member:
        return member.user_role in roles_needed

    return False

    
