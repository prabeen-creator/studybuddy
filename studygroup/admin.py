from django.contrib import admin
from django.apps import apps

Subject= apps.get_model('studygroup','Subject')
Course= apps.get_model('studygroup','Course')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('name','subject')
    list_filter=('subject',)
    


