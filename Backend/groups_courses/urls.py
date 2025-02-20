from django.urls import path
from .views import (
    CreateGroupAPIView, GroupListAPIView, GroupDetailAPIView,
    GroupMemberListAPIView, CreateGroupMemberAPIView, GroupMemberSelfDetailAPIView, GroupMembershipsDetailAPIView,
    GroupJoinRequestListAPIView, JoinRequestResponseAPIView,
    CoursesAPIView, CourseDetailAPIView
)

urlpatterns = [
    path('groups/', CreateGroupAPIView.as_view(), name='group_create'),
    path('groups/list/', GroupListAPIView.as_view(), name='group_list'),
    path('groups/<uuid:group_id>/', GroupDetailAPIView.as_view(), name='group_detail'),
    path('groups/<uuid:group_id>/members/', GroupMemberListAPIView.as_view(), name='group_member_list'),
    path('groups/<uuid:group_id>/members/create/', CreateGroupMemberAPIView.as_view(), name='group_member_create'),
    path('groups/<uuid:group_id>/members/self/', GroupMemberSelfDetailAPIView.as_view(), name='group_member_self_detail'),
    path('groups/<uuid:group_id>/members/<uuid:user_id>/', GroupMembershipsDetailAPIView.as_view(), name='group_member_detail'),
    path('groups/<uuid:group_id>/join-requests/', GroupJoinRequestListAPIView.as_view(), name='join_request_list'),
    path('join-requests/<uuid:join_request_id>/', JoinRequestResponseAPIView.as_view(), name='join_request_response'),
    path('groups/<uuid:group_id>/courses/', CoursesAPIView.as_view(), name='course_list'),
    path('courses/<uuid:course_id>/', CourseDetailAPIView.as_view(), name='course_detail'),
]
