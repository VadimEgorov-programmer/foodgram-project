from django.template import Library

from recipes.models import Purchase, Favorite
from users.models import Follow
from django.utils.http import urlencode

register = Library()

VARIANTS = (' рецепт ', ' рецепта ', ' рецептов ')


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def is_follower(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def is_favorite(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def is_purchase(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    query_string = context['request'].GET.copy()
    if 'page' in kwargs:
        query_string['page'] = kwargs.get('page')

    return query_string.urlencode()


@register.simple_tag(takes_context=True)
def manage_tags(context, **kwargs):
    tag = kwargs['tag']
    query_string = context['request'].GET.copy()
    tags = query_string.getlist('tags')
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    query_string.setlist('tags', tags)

    if 'page' in query_string:
        query_string.pop('page')

    return query_string.urlencode()


@register.filter
def declination(number, args):
    mod_10 = number % 10
    mod_100 = number % 100
    f_string = f'{number}'
    if mod_10 == 1 and mod_100 != 11:
        f_string += VARIANTS[0]
    elif mod_10 >= 2 and mod_10 <= 4 \
            and (mod_100 < 10 or mod_100 >= 20):
        f_string += VARIANTS[1]
    else:
        f_string += VARIANTS[2]
    return f_string


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.filter(name='url_parse')
def url_parse(request):
    filter_tags = ''
    for item in request.GET.getlist('filters'):
        filter_tags += f'&filters={item}'
    return filter_tags


@register.simple_tag
def full_page(request, page_num):
    path = request.get_full_path()
    current_page = request.GET.get('page')
    if 'tags' in path and 'page' in path:
        return path.replace(f'page={current_page}', f'page={page_num}')
    if 'tags' in path and 'page' not in path:
        return f'?page={page_num}&{path[2:]}'
    return f'?page={page_num}'