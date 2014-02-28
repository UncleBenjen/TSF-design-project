from django.contrib import admin
from curriculum.models import UserInfo
from curriculum.models import Department, Concept, Course, CourseInstance,Deliverable, LearningObjective, ProgramStream, Option, CEABUnit, CEABGrad

# Defining classes to customize admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','type')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'website')

class ConceptAdmin(admin.ModelAdmin):
    list_display = ('name','description','ceab_unit')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code','name','lecture_hours','lab_hours','credit','description','website','year')

class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date','textbook','semester','acc_math','acc_science','acc_eng_science','acc_eng_design','acc_comp')

class DeliverableAdmin(admin.ModelAdmin):
    list_display = ('type','percent','due_date','course_instance')

class LearningObjAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'course_instance')

class ProgramStreamAdmin(admin.ModelAdmin):
    list_display = ('name','description','department')

class OptionAdmin(admin.ModelAdmin):
	list_display= ('name', 'program_stream')

class CEABGradAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'measurement', 'average', 'attribute', 'course')

class CEABUnitAdmin(admin.ModelAdmin):
    list_display = ('name','description')

# Registering the models for the admin interface
admin.site.register(UserInfo, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInstance, CourseInstanceAdmin)
admin.site.register(Deliverable, DeliverableAdmin)
admin.site.register(LearningObjective, LearningObjAdmin)
admin.site.register(ProgramStream, ProgramStreamAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(CEABGrad, CEABGradAdmin)
admin.site.register(CEABUnit, CEABUnitAdmin)
