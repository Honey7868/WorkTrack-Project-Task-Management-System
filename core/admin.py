from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from .models import User, Project, Task, Comment, Attachment, TimeLog, Notification

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(TimeLog)
admin.site.register(Notification)

class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple('Users', False)
    )

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, commit=True):
        instance = super().save(commit)
        if commit:
            self.save_m2m()
        else:
            old_save_m2m = self.save_m2m
            def new_save_m2m():
                old_save_m2m()
                self.instance.user_set.set(self.cleaned_data['users'])
            self.save_m2m = new_save_m2m
        return instance

admin.site.unregister(Group)

class CustomGroupAdmin(GroupAdmin):
    form = GroupAdminForm
    fieldsets = (
        (None, {'fields': ('name', 'permissions', 'users')}),
    )

admin.site.register(Group, CustomGroupAdmin)
