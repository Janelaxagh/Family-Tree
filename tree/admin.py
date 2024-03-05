from django.contrib import admin
from django.db.models import Count
from .models import Family, FamilyMember, FamilyImage
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.site_header = "Древо"
admin.site.unregister(User)
admin.site.unregister(Group)


class MembersCountFilter(admin.SimpleListFilter):
    title = _('количество членов')
    parameter_name = 'members_count'

    def lookups(self, request, model_admin):
        return [
            ('0', _('Нет членов')),
            ('1', _('1 член')),
            ('2+', _('2 или более членов'))
        ]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(num_members=Count('members')).filter(num_members=0)
        if self.value() == '1':
            return queryset.annotate(num_members=Count('members')).filter(num_members=1)
        if self.value() == '2+':
            return queryset.annotate(num_members=Count('members')).filter(num_members__gte=2)


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1
    verbose_name = _('Член семьи')
    verbose_name_plural = _('Члены семьи')


class FamilyImageInline(admin.TabularInline):
    model = FamilyImage
    extra = 1
    verbose_name = _('Изображение семьи')
    verbose_name_plural = _('Изображения семей')


@admin.register(Family)
class FamilyAdmin(DraggableMPTTAdmin):
    inlines = [FamilyMemberInline, FamilyImageInline]
    list_display = ('tree_actions', 'indented_title', 'name', 'description', 'members_count')
    list_display_links = ('indented_title',)
    mptt_level_indent = 20
    list_filter = (MembersCountFilter,)
    verbose_name = _('Семья')
    verbose_name_plural = _('Семьи')

    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = _('Количество членов')


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'family', 'role')
    list_filter = ('family', 'role')
    verbose_name = _('Член семьи')
    verbose_name_plural = _('Члены семьи')


@admin.register(FamilyImage)
class FamilyImageAdmin(admin.ModelAdmin):
    list_display = ('family', 'image_preview')
    list_filter = ('family',)
    verbose_name = _('Изображение семьи')
    verbose_name_plural = _('Изображения семей')

    def image_preview(self, obj):
        return obj.image.url if obj.image else _('Нет изображения')
    image_preview.short_description = _('Предпросмотр изображения')


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    ordering = ('username',)
