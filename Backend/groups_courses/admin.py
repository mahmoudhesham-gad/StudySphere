from django.contrib import admin

# Register your models here.

from .models import Group, GroupMember, JoinRequest, Course
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'user')

class JoinRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'user')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(JoinRequest, JoinRequestAdmin)
admin.site.register(Course, CourseAdmin)