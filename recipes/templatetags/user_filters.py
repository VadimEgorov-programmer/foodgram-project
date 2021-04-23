from django.template import Library

from recipes.models import Purchase, Favorite
from users.models import Follow

register = Library()


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


@register.simple_tag(takes_context=True)
def get_purchases_count(context, **kwargs):
    return Purchase.objects.filter(user=context['request'].user).count()


@register.filter
def declination(number, args):
    args = [arg.strip() for arg in args.split(',')]
    last_number = int(number) % 10
    if last_number == 1:
        return f'{number} {args[0]}'
    elif last_number > 1 and last_number < 5:
        return f'{number} {args[1]}'
    elif last_number > 4 or last_number == 0:
        return f'{number} {args[2]}'
