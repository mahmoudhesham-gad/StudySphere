from rest_framework import serializers
from . import models


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ['id', 'name', 'group', 'min_value', 'max_value']
        read_only_fields = ['id', 'group']

class MaterialLabelSerializer(serializers.ModelSerializer):
    label = serializers.PrimaryKeyRelatedField(queryset=models.Label.objects.all())
    class Meta:
        model = models.MaterialLabel
        fields = ['label', 'number', 'material']
        read_only_fields = ['material']


class ViewMaterialLabelsSerializer(serializers.ModelSerializer):
    label = LabelSerializer()
    class Meta:
        model = models.MaterialLabel
        fields = ['label', 'number']
        read_only_fields = ['label', 'number']


class CreateMaterialSerializer(serializers.ModelSerializer):
    labels = MaterialLabelSerializer(many=True, required=False)

    class Meta:
        model = models.Material  
        fields = ['title', 'file', 'url', 'type', 'course', 'labels']
        read_only_fields = ['course']  

    def validate(self, data):
        validated_data = super().validate(data)
        file = validated_data.get('file')
        url = validated_data.get('url')
        if not file and not url:
            raise serializers.ValidationError("Either a file or a URL is required.")
        if file and url:
            raise serializers.ValidationError("Only one of file or URL should be provided, not both.")
        return validated_data

    def create(self, validated_data):
        labels_data = validated_data.pop('labels', [])
        material = models.Material.objects.create(**validated_data)
        for label_data in labels_data:
            models.MaterialLabel.objects.create(material=material, **label_data)
        return material
    
        

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = ['id', 'title', 'file', 'url', 'type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MaterialDetailSerializer(serializers.ModelSerializer):
        labels = serializers.SerializerMethodField()
        class Meta:
            model = models.Material
            fields = ['id', 'title', 'file', 'url', 'type', 'created_at', 'updated_at', 'labels']
            read_only_fields = ['id', 'created_at', 'updated_at']

        def get_labels(self, obj):
            material_labels = obj.labels.all()
            return [
                {
                    'label': label.label.name,
                    'number': label.number
                }
                for label in material_labels  
            ]
    
class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = ['id', 'title', 'file', 'url', 'type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'title', 'file', 'url', 'type', 'created_at', 'updated_at']



          
class MaterialLabelListSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='label.name')
    material = MaterialSerializer()  
    class Meta:
        model = models.MaterialLabel
        fields = ['label', 'number', 'material']
        read_only_fields = ['label', 'number', 'material']

class CreateMaterialCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialComment
        fields = ['material', 'Content', 'User']

class MaterialCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialComment
        fields = ['id', 'material', 'User', 'Content', 'CreatedAt']
        read_only_fields = ['id', 'material', 'User', 'CreatedAt']



