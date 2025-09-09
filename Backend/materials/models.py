from django.db import models
from groups_courses.models import Course, Group
from django.core.validators import FileExtensionValidator
from .validation import  VideoURLValidator, validate_file_size
from users.models import User
import uuid
# Create your models here.

def material_file_path(instance, filename):
    folder = instance.course.id
    return f'materials/{folder}/{filename}'

class Material(models.Model):
    TYPE = [
        ('document', 'Document'),
        ('url', 'URL'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to=material_file_path,  # use callable for dynamic path construction
        null=True, default=None,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt']),
            validate_file_size
        ],
    )
    url = models.URLField(
        null=True, default=None,
        validators=[VideoURLValidator()]  # Use the custom video URL validator
    )
    type = models.CharField(max_length=8, choices=TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        unique_together = ['title', 'course']
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(file__isnull=False) |
                    models.Q(url__isnull=False)
                ),
                name='file_or_url_required'
            )
        ]




    def __str__(self):
        return self.title

class Label(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='labels')
    min_value = models.PositiveIntegerField()
    max_value = models.PositiveIntegerField()

    class Meta:
        unique_together = ['name', 'group']

    def __str__(self):
        return self.name

class MaterialLabel(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='labels')
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ['material', 'label']


class MaterialComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material = models.ForeignKey(Material, null=False,  on_delete=models.CASCADE)
    User = models.ForeignKey(User, null=False,  on_delete=models.CASCADE)
    Content = models.TextField(null=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.User} on material {self.material}"
