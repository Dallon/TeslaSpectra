from django import template
register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name = 'addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    new_string = str(arg1 + arg2)
    return str(new_string)