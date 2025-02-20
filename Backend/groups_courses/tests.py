from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Group, GroupMember, JoinRequest, Course
from users.models import User

class GroupTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password')
        self.other_user = User.objects.create_user(email='otheruser@example.com', username='otheruser', password='password')
        self.client.force_authenticate(user=self.user)
        self.group_data = {
            "name": "Study Group",
            "description": "A group for studying",
            "join_type": "open",
            "post_permission": "members",
            "edit_permissions": "admins"
        }

    def test_create_group(self):
        url = reverse('group_create')
        response = self.client.post(url, self.group_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().name, 'Study Group')

    def test_list_groups(self):
        Group.objects.create(owner=self.user, **self.group_data)
        url = reverse('group_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_group(self):
        group = Group.objects.create(owner=self.user, **self.group_data)
        url = reverse('group_detail', args=[group.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Study Group')

    def test_update_group_permission_denied(self):
        group = Group.objects.create(owner=self.user, **self.group_data)
        self.client.force_authenticate(user=self.other_user)
        url = reverse('group_detail', args=[group.id])
        response = self.client.put(url, self.group_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_permission_denied(self):
        group = Group.objects.create(owner=self.user, **self.group_data)
        self.client.force_authenticate(user=self.other_user)
        url = reverse('group_detail', args=[group.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class GroupMemberTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password')
        self.other_user = User.objects.create_user(email='otheruser@example.com', username='otheruser', password='password')
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(owner=self.user, name="Study Group", join_type="invite", post_permission="members", edit_permissions="admins")
        self.member_data = {
            "user": self.other_user.id
        }

    def test_create_group_member(self):
        url = reverse('group_member_create', args=[self.group.id])
        response = self.client.post(url, self.member_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GroupMember.objects.count(), 1)
        self.assertEqual(GroupMember.objects.get().user.id, self.member_data['user'])

    def test_list_group_members(self):
        GroupMember.objects.create(group=self.group, user=self.user, user_role='member')
        url = reverse('group_member_list', args=[self.group.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_group_member(self):
        member = GroupMember.objects.create(group=self.group, user=self.user, user_role='member')
        url = reverse('group_member_detail', args=[self.group.id, member.user.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_create_group_member_permission_denied(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('group_member_create', args=[self.group.id])
        response = self.client.post(url, self.member_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_member_permission_denied(self):
        member = GroupMember.objects.create(group=self.group, user=self.user, user_role='member')
        self.client.force_authenticate(user=self.other_user)
        url = reverse('group_member_detail', args=[self.group.id, member.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class JoinRequestTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(owner=self.user, name="Study Group", join_type="open", post_permission="members", edit_permissions="admins")
        self.join_request_data = {
            "group": self.group.id,
            "user": self.user.id
        }

    def test_list_join_requests(self):
        JoinRequest.objects.create(group=self.group, user=self.user)
        url = reverse('join_request_list', args=[self.group.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class CourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password')
        self.other_user = User.objects.create_user(email='otheruser@example.com', username='otheruser', password='password')
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(owner=self.user, name="Study Group", join_type="open", post_permission="members", edit_permissions="admins")
        self.course_data = {
            "name": "Course Name",
            "description": "Course Description",
        }

    def test_create_course(self):
        url = reverse('course_list', args=[self.group.id])
        response = self.client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().group, self.group)

    def test_create_duplicate_course(self):
        Course.objects.create(group=self.group, name="Course Name", description="Course Description")
        url = reverse('course_list', args=[self.group.id])
        response = self.client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_courses(self):
        Course.objects.create(group=self.group, name="Course Name", description="Course Description")
        url = reverse('course_list', args=[self.group.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_course(self):
        course = Course.objects.create(group=self.group, name="Course Name", description="Course Description")
        url = reverse('course_detail', args=[course.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Course Name')

    def test_create_course_permission_denied(self):
        # Ensure other_user is not a member of the group
        self.assertFalse(GroupMember.objects.filter(group=self.group, user=self.other_user).exists())
        self.client.force_authenticate(user=self.other_user)
        url = reverse('course_list', args=[self.group.id])
        response = self.client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_permission_denied(self):
        course = Course.objects.create(group=self.group, name="Course Name", description="Course Description")
        self.client.force_authenticate(user=self.other_user)
        url = reverse('course_detail', args=[course.id])
        response = self.client.put(url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_permission_denied(self):
        course = Course.objects.create(group=self.group, name="Course Name", description="Course Description")
        self.client.force_authenticate(user=self.other_user)
        url = reverse('course_detail', args=[course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
