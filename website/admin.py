from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(models.About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_description',
                    'companyimage', 'companylogo', 'is_active']
    list_display_links = ['companylogo']
    list_editable = ['company_name', 'company_description',
                     'is_active']

    def companyimage(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.company_image.url,
            width=100,
            height=150,
        )
        )

    def companylogo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.company_logo.url,
            width=100,
            height=150,
        )
        )


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog_title', 'blog_description',
                    'image', 'blog_image', 'created_date', 'updated_on']
    list_display_links = ['id']
    list_editable = ['blog_title', 'blog_description',
                     'blog_image']

    def image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.blog_image.url,
            width=100,
            height=150,
        )
        )


@admin.register(models.Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',
                    'description', 'image',
                    'service_image']
    list_display_links = ['id']
    list_editable = ['name',
                     'description',
                     'service_image']

    def image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.service_image.url,
            width=100,
            height=150,
        )
        )


class TeamInline(admin.TabularInline):
    model = models.Team
    fields = ('name', 'designation')


class HomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'experts', 'running_project']
    list_display_links = ['id']
    list_editable = ['client', 'experts', 'running_project']
    inlines = [TeamInline]


admin.site.register(models.Home, HomeAdmin)
admin.site.register(models.SocialLinks)
admin.site.register(models.Comment)
admin.site.register(models.Contact)
admin.site.register(models.ContactUs)
admin.site.register(models.Team)
admin.site.register(models.Testimonial)
