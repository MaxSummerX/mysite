from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).exclude(total_comments=0).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

import os

@register.simple_tag
def file_link_with_icon(file_url):

    icons = {
        'pdf': 'pdf.svg',
        'doc': 'doc.svg',
        'docx': 'docx.svg',
        'xls': 'xls.svg',
        'xlsx': 'xlsx.svg'
    }

    file_name = file_url.split('/')[-1].lower()
    file_type = file_name.split('.')[-1]
    icons_type = icons.get(file_type, 'default.svg')

    return mark_safe(f"""
    <a href="{file_url}" download title="Скачать файл {file_name}">
    <img src="/static/icons/{icons_type}" width="32" height="32" alt="{file_type}" />
    {file_name}</a>""")