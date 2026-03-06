from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import AppLog, Book, Borrow, CustomUser, Favorite
# Register your models here.

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with a required username field.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('user_name', 'first_name', 'last_name', 'email')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('user_name', 'email','first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('user_name','email', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name','profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name','email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    
    
@admin.register(AppLog)
class AppLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level', 'status_code', 'method', 'path', 'created_at')
    list_filter = ('level', 'status_code', 'method', 'created_at', 'user')
    search_fields = ('message', 'path', 'event', 'user__user_name', 'user__email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Favorite)
