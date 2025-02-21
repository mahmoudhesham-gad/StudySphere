from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Material)
admin.site.register(models.MaterialComment)
admin.site.register(models.Label)
admin.site.register(models.MaterialLabel)

