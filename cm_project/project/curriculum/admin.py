from django.contrib import admin
from curriculum.models import UserInfo
from curriculum.models import Department, Concept, Course, CourseInstance,Textbook, Deliverable, LearningObjective, ProgramStream, Option, ContactHours, CEABGrad, Measurement, StudentGroup

# Defining classes to customize admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','type')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'website')

class ConceptAdmin(admin.ModelAdmin):
    list_display = ('name','description','ceab_unit')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code','name','lecture_hours','lab_hours','tut_hours','credit','description','website','year')

class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date','semester','acc_math','acc_science','acc_eng_science','acc_eng_design','acc_comp')

class TextbookAdmin(admin.ModelAdmin):
    list_display = ('name','required','isbn','instance')

class DeliverableAdmin(admin.ModelAdmin):
    list_display = ('type','percent','due_date','course_instance')

class LearningObjAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'course_instance')

class ProgramStreamAdmin(admin.ModelAdmin):
    list_display = ('name','description','department')

class OptionAdmin(admin.ModelAdmin):
	list_display= ('name', 'program_stream')

class CEABGradAdmin(admin.ModelAdmin):
	list_display = ('name', 'date', 'measurement_text','measurement_file','rubrik','attribute', 'course')
	filter_horizontal = ('student_groups',)

class MeasurementAdmin(admin.ModelAdmin):
	list_display = ('ceab_grad','students','level1','level2','level3','level4','average')

class StudentGroupAdmin(admin.ModelAdmin):
	list_display = ('instance','size','type')

class ContactHoursAdmin(admin.ModelAdmin):
    list_display = ('instance','contact_es','contact_ed','contact_ma','contact_sc','contact_co')

# Registering the models for the admin interface
admin.site.register(UserInfo, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInstance, CourseInstanceAdmin)
admin.site.register(Textbook, TextbookAdmin)
admin.site.register(Deliverable, DeliverableAdmin)
admin.site.register(LearningObjective, LearningObjAdmin)
admin.site.register(ProgramStream, ProgramStreamAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(CEABGrad, CEABGradAdmin)
admin.site.register( StudentGroup, StudentGroupAdmin)
admin.site.register( Measurement, MeasurementAdmin)
admin.site.register(ContactHours,ContactHoursAdmin)
