from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError 
from rest_framework.response import Response

from . import models, serializers
from .permissions import can_edit_members, has_higher_role, ensure_can_edit_members, ensure_group_owner


# Create your views here.
class CreateGroupAPIView(generics.CreateAPIView):
    """
    This view is used to create a new group
    
    Endpoint: `/groups/`
    Methods: POST
    Permissions: IsAuthenticated
    """
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupListAPIView(generics.ListAPIView):
    """
    This view is used to list all groups

    Endpoint: `/groups/`
    Methods: GET
    Permissions: AllowAny
    """
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.filter(join_type__in=['open', 'request']).all()
    permission_classes = [AllowAny,]
    search_fields = ['name', 'description']
    filterset_fields = ['join_type']
    
    

class OwnedGroupListAPIView(generics.ListAPIView):
    """
    This view is used to list all groups owned by the user

    Endpoint: `/user/groups/`
    Methods: GET
    Permissions: IsAuthenticated
    """
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return models.Group.objects.filter(owner=self.request.user)


class GroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view is used to view, update, or delete a specific group 
    
    Endpoint: `/groups/<group_id>/`
    Methods: GET, PUT, DELETE
    Permissions: IsAuthenticated (user must be a member of the group)
        - GET: Open to all group members
        - PUT, DELETE: group owner only
    """
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    lookup_url_kwarg = 'group_id'
    lookup_field = 'id'

    def get_queryset(self):
        """
        This method is used to override the queryset for the view
        to improve performance by reducing the number of queries
        by prefetching related fields
        """
        group_id = self.kwargs.get(self.lookup_url_kwarg)
        return models.Group.objects.select_related('owner').prefetch_related('members').filter(id=group_id)

    def get_object(self):
        group = self.get_queryset().first()
        if group is None:
            raise NotFound(
                detail="Group not found",
                code=status.HTTP_404_NOT_FOUND,
            )
        # Check if user is a member of the group
        if group.owner == self.request.user or any(member.user == self.request.user for member in group.members.all()):
            return group
        else:
            raise PermissionDenied(
                detail="You are not a member of this group",
                code=status.HTTP_403_FORBIDDEN,
            )
    
    def perform_update(self, serializer):
        group = self.get_object()
        if group.owner != self.request.user:
            raise PermissionDenied(
                detail="User doesn't have permission to update this group",
                code=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()

    def perform_destroy(self, instance):
        group = self.get_object()
        if group.owner != self.request.user:
            raise PermissionDenied(
                detail="User doesn't have permission to delete this group",
                code=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()


class GroupMemberListAPIView(generics.ListAPIView):
    """
    
    Endpoint: `/groups/<group_id>/members/`
    Methods: GET
    Permissions: IsAuthenticated (user must be a member of the group)
        - GET: Open to all members
    """
    serializer_class = serializers.GroupMemberSerializer
    queryset = models.GroupMember.objects.all()
    lookup_url_kwarg = 'group_id'
    lookup_field = 'group_id'

    def get_queryset(self):
        group_id = self.kwargs.get(self.lookup_url_kwarg)
        group = get_object_or_404(
            models.Group.objects.prefetch_related('members'),
            id=group_id
        )
        ensure_can_edit_members(self.request.user, group, message="User doesn't have permission to view group members")
        return group.members.all()

            
class CreateGroupMemberAPIView(generics.CreateAPIView):
    """
    This view is used to add a new member to a group
    
    Endpoint: `/groups/<group_id>/members/create/`
    Methods: POST
    Permissions: IsAuthenticated (user must be a member of the group)
        - POST: members with edit permissions only
    """
    serializer_class = serializers.CreateGroupMemberSerializer
    permission_classes = [IsAuthenticated,]


    def _try_save_membership(self, serializer, group):
        try:
            serializer.save(group=group)
        except IntegrityError:
            raise ValidationError(
                detail="User is already a member of this group",
                code=status.HTTP_400_BAD_REQUEST,
            )
    

    def perform_create(self, serializer):
        user = self.request.user
        group = get_object_or_404(
            models.Group.objects.prefetch_related("members"),
            id=self.kwargs.get('group_id')
        )
        
        if serializer.validated_data.get('user') == group.owner:
            raise ValidationError(
                detail="Owner can't be a member of his group",
                code=status.HTTP_400_BAD_REQUEST,
            )

        if can_edit_members(user, group):
            self._try_save_membership(serializer, group)
            return
                        
        if group.join_type == 'open':
            self._try_save_membership(serializer, group)

        elif group.join_type == 'request':
            models.JoinRequest.objects.create(group=group, user=user)
        
        elif group.join_type == 'invite':
            raise PermissionDenied(
                detail="User must be invited to join this group",
                code=status.HTTP_403_FORBIDDEN,
            )
        else:
            raise ValidationError(  
                detail="Invalid join type",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            

class GroupMemberSelfDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    This view is used to get user's membership in a group or leave a group
    
    Endpoint: `/groups/<group_id>/leave_group/`
    Methods: GET, DELETE
    Permissions: IsAuthenticated (user must be a member of the group)
        - GET: Open to all members, returns
        - DELETE: User can leave the group
    """
    serializer_class = serializers.GroupMemberSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        return models.GroupMember.objects.filter(
            group=self.kwargs.get(self.lookup_url_kwarg), user=self.request.user
        )


class GroupMembershipsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view is used to view, update, or delete a specific group membership
    
    Endpoint: `/groups/<group_id>/members/<user_id>/`
    Methods: GET, PUT, DELETE
    Permissions: IsAuthenticated (user must be a member of the group)

    - GET: members with edit permissions only
    - PUT: group owner only
    - DELETE: members with edit permissions only

    """
    serializer_class = serializers.GroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.GroupMember.objects.select_related('user', 'group').filter(
            group_id=self.kwargs.get("group_id"), user=self.kwargs.get("user_id")
        )

    def get_object(self):
        """
        only users that have permission to edit the group members can view group members
        """
        membership = get_object_or_404(self.get_queryset())
        ensure_can_edit_members(self.request.user, membership.group, message="User doesn't have permission to view group members")
        return membership

    def update(self, request, *args, **kwargs):
        """
        user can only update group member roles if they are the group owner
        """
        membership = self.get_object()
        ensure_group_owner(self.request.user, membership.group, message="User doesn't have permission to update group members")
        
        serializer = self.get_serializer(membership, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """
        user can only delete group member if they have higher role
        """
        if has_higher_role(self.request.user, instance.user):
            instance.delete()
        else:
            raise PermissionDenied(
                detail="User doesn't have permission to delete this group member",
                code=status.HTTP_403_FORBIDDEN,
            )


class GroupJoinRequestListAPIView(generics.ListAPIView):
    """
    This view is used to list all join requests for a group
    
    Endpoint: `/groups/<group_id>/join_requests/`
    Methods: GET
    Permissions: IsAuthenticated (user must be a member of the group)
    """
    serializer_class = serializers.GroupJoinRequestSerializer
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        group = get_object_or_404(
            models.Group.objects.prefetch_related('join_requests', 'members'),
            id=self.kwargs.get('group_id')
        )
        ensure_can_edit_members(self.request.user, group, message="User doesn't have permission to view join requests")
        return group.join_requests.all()


class JoinRequestResponseAPIView(APIView):
    """
    This view is used to respond to a join request
    
    Endpoint: `/join_requests/<join_request_id>/`
    Methods: POST
    expected data: {"action": "accept" | "decline"}
    Permissions: IsAuthenticated (user must be a member of the group)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, join_request_id):
        join_request = get_object_or_404(models.JoinRequest.objects.select_related('group'), id=join_request_id)
        group = join_request.group

        ensure_can_edit_members(request.user, group, message="User doesn't have permission to respond to join requests")

        if request.data.get('action') == 'accept':
            try:
                models.GroupMember.objects.create(
                    group=group,
                    user=join_request.user
                )
            except IntegrityError:
                raise ValidationError(
                    detail="User is already a member of this group",
                    code=status.HTTP_400_BAD_REQUEST
                )
            join_request.delete()
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "User added to group"}
            )
        
        elif request.data.get('action') == 'decline':
            join_request.delete()
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Join request declined"}
            )
        
        else:
            raise ValidationError(
                detail="Invalid action",
                code=status.HTTP_400_BAD_REQUEST
            )


class CoursesAPIView(APIView):
    """
    This view is used to list and create courses for a group

    Endpoint: `/groups/<group_id>/courses/`
    Methods: GET, POST
    Permissions: IsAuthenticated
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(
            models.Group.objects.prefetch_related('members', 'courses'),
            id=group_id
        )

        # using any() to check if user is a member of the group without needing to hit the database since members are prefetched
        if group.owner == request.user or any(member.user == request.user for member in group.members.all()):
            courses = group.courses.all()
            serializer = serializers.CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied(
                detail="User is not a member of this group",
                code=status.HTTP_403_FORBIDDEN,
            )
        
    def _check_group_admin(self, group, user):
        for member in group.members.all():
            if member.user == user:
                if member.user_role == 'admin':
                    return True
                else:
                    return False
        return False
        
    def post(self, request, group_id):
        group = get_object_or_404(
            models.Group.objects.prefetch_related('members'),
            id=group_id
        )
        if not (group.owner == request.user or self._check_group_admin(group, request.user)):
            raise PermissionDenied(
                detail="User doesn't have permission to create courses in this group",
                code=status.HTTP_403_FORBIDDEN,
            )
            
        serializer = serializers.CreateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(group=group)
        except IntegrityError:  
            raise ValidationError(
                detail="Course with this name already exists",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view is used to view, update, or delete a specific course

    Endpoint: `/courses/<course_id>/`
    Methods: GET, PUT, DELETE
    Permissions: IsAuthenticated, user must be a admin or owner of the group
    """

    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'course_id'
    lookup_field = 'id'

    def get_object(self):
        course = get_object_or_404(
            models.Course.objects.select_related('group__owner'),
            id=self.kwargs.get('course_id')
        )
        if course.group.owner == self.request.user:
            return course
        
        raise PermissionDenied(
            detail="Only the group owner can edit this course",
            code=status.HTTP_403_FORBIDDEN,
        )

