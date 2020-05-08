from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

#creating a simple tag

register = template.Library()

#simple tags returns a string
@register.simple_tag
def total_posts():
    return Post.published.count()

#inclusion tags that returns templates
@register.inclusion_tag('templates/blog/post/latest_post.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    print(latest_posts)
    return {'latest_posts' : latest_posts }

#simple tags that returns a...
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

#markdown function
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))