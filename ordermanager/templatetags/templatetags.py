import markdown
from django import template
from django.utils.safestring import mark_safe
from django.template.defaulttags import register

register = template.Library()


# 마크다운 적용시켜주는 필터
@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

@register.filter()
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()