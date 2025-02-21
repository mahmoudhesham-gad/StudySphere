from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from groups_courses.models import GroupMember
from groups_courses.permissions import can_post, check_group_admin
from . import models, serializers


# Create your views here.
class CreateMaterialAPIView(generics.CreateAPIView):
    """
    API view for creating materials.

    This view is used to create materials.
    The user must be authenticated to create a material.

    Endpoint: `/api/course/<course_id>/materials/create/`
    Method: POST
    Permissions: IsAuthenticated (User must be authenticated)
    """

    serializer_class = serializers.CreateMaterialSerializer
    queryset = models.Material.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        course = get_object_or_404(
            models.Course.objects.select_related('group'),
            id=self.kwargs.get('course_id')
            )
        if can_post(self.request.user, course.group):
            try:
                serializer.save(owner=self.request.user, course=course)
            except IntegrityError:
                raise ValidationError(
                    {"detail": "Either a file or a URL is required."},
                    code=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to post materials in this course."},
                code=status.HTTP_403_FORBIDDEN
            )

class MaterialListAPIView(generics.ListAPIView):  
    """
    API view for listing materials.

    Endpoint: `/api/course/<course_id>/materials/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializers.MaterialSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        # Retrieve the course, or 404 if not found.
        course = get_object_or_404(models.Course.objects.select_related('group'), id=course_id)
        # Assume the Course model has a related `group` field.
        # If course.group is a queryset, you may need to adjust accordingly.
        if course.group.owner == self.request.user or GroupMember.objects.filter(user=self.request.user, group=course.group).exists():
            return models.Material.objects.filter(course=course)
        else:  
            raise PermissionDenied(
                {"detail": "You do not have permission to view materials in this course."},
                code=status.HTTP_403_FORBIDDEN
            )
        
class MaterialDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for updating and deleting materials.

    This view is used to update and delete materials.
    The user must be authenticated to update and delete a material.
    The user can only delete their own materials.

    Endpoint: `/api/materials/<material_id>/`
    Method: DELETE, PUT
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializers.MaterialDetailSerializer
    queryset = models.Material.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_url_kwarg = 'material_id'
    lookup_field = 'id'

    def get_queryset(self):
        material_id = self.kwargs.get('material_id')
        return models.Material.objects.filter(id=material_id).select_related('owner', 'course__group').all()
        
    

    def perform_destroy(self, instance):
        if instance.owner == self.request.user or can_delete_material(self.request.user, instance.course.group):
            instance.delete()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this material."},
                code=status.HTTP_403_FORBIDDEN
            )

    def perform_update(self, serializer):
        if serializer.instance.owner == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this material."},
                code=status.HTTP_403_FORBIDDEN
            )
    
class ListCreateLabelAPIView(generics.ListCreateAPIView):
    """
    API view for creating labels.

    This view is used to list and create group labels.
    The user must be authenticated to create a label.

    Endpoint: `/api/groups/<group_id>/labels/`
    Method: GET, POST
    Permissions: IsAuthenticated, GroupAdmin (User must be authenticated and be owner or admin of the group)
    """
    serializer_class = serializers.LabelSerializer
    queryset = models.Label.objects.all()
    lookup_url_kwarg = 'group_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated,]

    
    def perform_create(self, serializer):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(models.Group, id=group_id)
        if check_group_admin(self.request.user, group):
            serializer.save(group=group)
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to create labels in this group."},
                code=status.HTTP_403_FORBIDDEN
            )

class MaterialLabelsAPIView(APIView):
    """
    API view for creating material labels.

    This view is used to create labels for a material.
    The user must be authenticated to create a label.

    Endpoint: `/api/materials/<material_id>/labels/`
    Method: GET, POST
    Permissions: IsAuthenticated (User must be authenticated)

    GET: Data is returned in the following format:  
    ```
    [
        {
            "label": {
                "id": 1,
                "name": "label 1",
                "group": 1
            },
            "number": 1
        }
    ]
    ```
    POST: Data should be sent in the following format:
    ```
    {
        "labels": [
            {
                "label": label_id,
                "number": label_index
            }
        ]
    }
    ```

    """
    permission_classes = [IsAuthenticated,]

    def _user_material_permission(self, material):
        if self.request.user != material.owner:
            raise PermissionDenied(
                {"detail": "You do not have permission to add labels to this material."},
                code=status.HTTP_403_FORBIDDEN
            )
    
    def get(self, request, material_id):
        material = get_object_or_404(models.Material, id=material_id)
        self._user_material_permission(material)
        material_labels = models.MaterialLabel.objects.filter(material=material).prefetch_related('label').all()
        
        return Response(serializers.ViewMaterialLabelsSerializer(material_labels, many=True).data)
        
    
    def put(self, request, material_id):
        material = get_object_or_404(models.Material, id=material_id)
        self._user_material_permission(material)

        labels_data = request.data.get('labels', [])
        if not labels_data:
            material.labels.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = serializers.MaterialLabelSerializer(data=labels_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(material=material)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MaterialLabelListAPIView(APIView):
    """
    list materials by a given Label

    Endpoint: `/api/course/<course_id>/materials/labels/<label_id>/`

    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)

    returns 
    ```
    {
        "label_name": "label_name",
        "materials": {
            "label_index": [
                { 
                    "material": {
                        "id": material_id,
                        "title": "material_title",
                        "file": "file_path",
                        "url": "url_path",
                        "type": "material_type",
                        "created_at": "created_at",
                        "updated_at": "updated_at"
                    }
                }
            ]
        }
    }
    ```
    """
    permission_classes = [IsAuthenticated,]

    def get(self, request, course_id, label_id):
        course = get_object_or_404(models.Course, id=course_id)
        if course.group.owner == self.request.user or GroupMember.objects.filter(user=self.request.user, group=course.group).exists():
            materials = models.MaterialLabel.objects.filter(label=label_id, material__course=course).select_related('material', 'label').all()
            grouped_data = {}
            label_name = materials[0].label.name if materials else ""
            for material_label in materials:
                label_index = material_label.number
                if label_index not in grouped_data:
                    grouped_data[label_index] = []
                grouped_data[label_index].append({
                    "material": serializers.MaterialListSerializer(material_label.material).data
                })
            return Response({
                "label_name": label_name,
                "materials": grouped_data
            })
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to view materials in this course."},
                code=status.HTTP_403_FORBIDDEN
            )

class CreateMaterialCommentsAPIView(generics.CreateAPIView):
    """
    API view for creating comments on material.

    This view is used to create comments on a material.
    The user must be authenticated to create a comment.

    Endpoint: `/api/comments/create/`
    Method: POST
    Permissions: IsAuthenticated (User must be authenticated)
    """

    serializer_class = serializers.CreateMaterialCommentsSerializer
    queryset = models.MaterialComment.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

class MaterialCommentsListAPIView(generics.ListAPIView):
    """
    API view for listing material comments.

    This view is used to list material comments.
    The user must be authenticated to view comments.

    Endpoint: `/api/materials/<material_id>/comments/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializers.MaterialCommentSerializer
    queryset = models.MaterialComment.objects.order_by('-CreatedAt')
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        material_id = self.kwargs.get('material_id')
        return models.MaterialComment.objects.filter(material=material_id).all()

class MaterialCommentsDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for updating and deleting comments on material.

    This view is used to update and delete comments on a material.
    The user must be authenticated to update and delete a comment.
    The user can only delete their own comments.

    Endpoint: `/api/comments/<comment_id>/`
    Method: DELETE, PUT
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializers.MaterialCommentSerializer
    queryset = models.MaterialComment.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_url_kwarg = 'comment_id'
    lookup_field = 'id'

    def perform_destroy(self, instance):
        if instance.User == self.request.user or instance.material.Owner == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this comment."},
                code=status.HTTP_403_FORBIDDEN
            )

    def perform_update(self, serializer):
        if serializer.instance.User == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this comment."},
                code=status.HTTP_403_FORBIDDEN
            )

