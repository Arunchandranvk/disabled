from django import template

register = template.Library()

@register.filter
def file_extension(value):
    return value.name.split('.')[-1].lower()