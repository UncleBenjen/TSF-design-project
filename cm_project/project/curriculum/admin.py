from django.contrib import admin
from curriculum.models import UserInfo, Department, Concept, Course, CourseInstance,Deliverable, LearningObjective, ProgramStream, CEABUnit, CEABGrad

# Defining classes to customize admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','type', 'email')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'website')

class ConceptAdmin(admin.ModelAdmin):
    list_display = ('name','description','highschool','ceab_unit','related_concepts')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','credit','description','website','year','department','pre_requisites','anti_requisites','co_requisites')

class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('name','course','professors','assistants','semester','acc_math','acc_science','acc_eng_science','acc_eng_design','acc_comp','concepts')

class DeliverableAdmin(admin.ModelAdmin):
    list_display = ('type','percent','due_date','course_instance')

class LearningObjAdmin(admin.ModelAdmin):
    list_display = ('name','description','related_concepts', 'course_instance')

class ProgramStreamAdmin(admin.ModelAdmin):
    list_display = ('name','description','department','courses')

class CEABGradAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'measurement', 'average', 'attribute', 'course')

class CEABUnitAdmin(admin.ModelAdmin):
    list_display = ('name','description')

# Registering the models for the admin interface
admin.site.register(UserInfo, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Concept)
admin.site.register(Course)
admin.site.register(CourseInstance)
admin.site.register(Deliverable)
admin.site.register(LearningObjective)
admin.site.register(ProgramStream)
admin.site.register(CEABGrad)
admin.site.register(CEABUnit)
