from django import template

register = template.Library()


@register.filter
def get_all_projects(queryset):
    return ", ".join([project.name for project in queryset])