from django.urls import path
from . import views

urlpatterns = [
    path('course/<uuid:course_id>/materials/create/', views.CreateMaterialAPIView.as_view(), name='create_material'),
    path('course/<uuid:course_id>/materials/', views.MaterialListAPIView.as_view(), name='list_materials'),  
    path('materials/<uuid:material_id>/', views.MaterialDestroyUpdateAPIView.as_view(), name='update_delete_material'),
    path('groups/<uuid:group_id>/labels/', views.ListCreateLabelAPIView.as_view(), name='list_create_labels'),
    path('materials/<uuid:material_id>/labels/', views.MaterialLabelsAPIView.as_view(), name='material_labels'),
    path('course/<course_id>/materials/labels/<label_id>/', views.MaterialLabelListAPIView.as_view(), name='materials_by_label'),
    path('comments/create/', views.CreateMaterialCommentsAPIView.as_view(), name='create_material_comment'),
    path('materials/<uuid:material_id>/comments/', views.MaterialCommentsListAPIView.as_view(), name='list_material_comments'),
    path('comments/<uuid:comment_id>/', views.MaterialCommentsDestroyUpdateAPIView.as_view(), name='update_delete_material_comment'),
]
