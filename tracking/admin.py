from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from .models import *

admin.site.register(Clinic)
admin.site.register(ClinicUser)
admin.site.register(Organization)
admin.site.register(ReferringEntity)
admin.site.register(TreatingProvider)
admin.site.register(PatientVisit)
admin.site.register(ReferringReportSetting)


def user_activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
user_activate.short_description = "Activate user"


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    actions = [user_activate]

    @staticmethod
    def save_model(request, obj, form, change):
        # Override this to set the password to the value in the field if it's
        # changed.
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
