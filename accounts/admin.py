from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Accounts, PasswordResetCode, Service

# tou a ter uns bugs básicos aqui 
'''
class ServiceInline(admin.StackedInline):
    model: Service
    can_delete = False
    verbose_name_plural = 'Serviços'

class CustomAccountsAdmin(UserAdmin):
    # protecção para os staffs não verem outros staffs
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True, is_staff=True)
            return qs
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser and obj is not None:
            form.base_fields['username'].disable = True
            form.base_fields['is_superuser'].disable = True
            form.base_fields['user_permissions'].disable = True
            form.base_fields['groups'].disable = True
            form.base_fields['is_active'].disabled = True
            form.base_fields['is_staff'].disable = True
            form.base_fields['creation_date'].disable = True

        return form
    
    inlines = (ServiceInline)
    list_display = ('username', 'email', 'is_verified', 'creation_date')
    search_fields = ['username', 'first_name', 'last_name', 'email', 'is_verified', 'is_service']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'is_service')}),
        ('Permissões', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # garantia que um usuário tenha apenas um perfil
        if not obj.pk and not change:
            # verificar se o usário já possui um perfil
            if Service.objects.filter(user=obj).exists:
                raise ValueError('Este usuário já possui uma conta de serviço.')
            
            Service.objects.create(user=obj)

    def get_inline_instances(self, request, obj=None):
        return [Service(self.model, self.admin_site)]
        ##return super().get_inline_instances(request, obj)

admin.site.register(Accounts, CustomAccountsAdmin)'''
admin.site.register(Accounts)
admin.site.register(PasswordResetCode)
admin.site.register(Service)