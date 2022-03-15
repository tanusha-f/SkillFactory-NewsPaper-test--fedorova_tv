from django import template

register = template.Library()


@register.filter(name='mult')
def mult(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')


@register.filter(name='censor')
def censor(text):
    cens_list = ['word1', 'word2', 'word3']
    for word in cens_list:
        text = text.replace(word, '*' * len(word))
    return text
