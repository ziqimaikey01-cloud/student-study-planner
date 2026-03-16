from django.contrib import admin
from .models import Course, Assignment
# Register your models here.
# admin.site.register(Course)
# admin.site.register(Assignment)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'owner')
    search_fields = ('name', 'code', 'owner__username')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'completed')
    search_fields = ('title', 'course__name')
    list_filter = ('completed',)