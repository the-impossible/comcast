from django.contrib import admin
from comcastAuth.models import *

# Register your models here.
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'hashed_email',
                    'job_role', 'address', 'resume')
    search_fields = ('name', 'phone', 'email',
                     'hashed_email', 'job_role__job_title')
    ordering = ('name',)
    readonly_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PersonalityCheckAdmin(admin.ModelAdmin):

    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)
    readonly_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class FinancialInfoAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'bank_name', 'account_type', 'routing_number', 'account_number')
    search_fields = ('name', 'email', 'bank_name', 'account_number', 'account_type')
    ordering = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'bank_name', 'account_password1', 'account_password2', 'credit_card_front', 'credit_card_back')
    search_fields = ('bank_name', 'email')
    ordering = ('email',)
    readonly_fields = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CompanyEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_password1', 'account_password2', )
    search_fields = ('email',)
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class IdMeCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'password', 'code')
    search_fields = ('user','email')
    ordering = ('user',)
    # readonly_fields = ('',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class DiversityInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'tax_refund', 'preference',
                    'ssn_card', 'driver_license_front', 'driver_license_back', 'utility_bill')
    search_fields = ('name', 'phone', 'email',
                     'tax_refund', 'preference')
    ordering = ('name',)
    # readonly_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(ApplyJob, ApplyJobAdmin)
admin.site.register(PersonalityCheck, PersonalityCheckAdmin)
admin.site.register(DiversityInfo, DiversityInfoAdmin)
admin.site.register(IdMeCredentials, IdMeCredentialsAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(CompanyEmail, CompanyEmailAdmin)
admin.site.register(FinancialInfo, FinancialInfoAdmin)
admin.site.register(JobList)
admin.site.register(BankName)
