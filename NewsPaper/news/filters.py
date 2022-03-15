from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter
from .models import Post, Author
from django.forms.widgets import DateInput


class PostFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        auth = []
        for names in Author.objects.all().order_by('user__username').values('id', 'user__username'):
            auth.append((names.get('id'), names.get('user__username')))
        self.filters['author'].extra.update(
            {
                'choices': auth
            }
        )

    author = ChoiceFilter(field_name='author', label='Имя автора')
    title = CharFilter(field_name='head', lookup_expr='icontains',
                       label='Заголовок статьи')
    data = DateFilter(field_name='time_in', lookup_expr='gt',
                      label='Опубликовано не ранее', widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ('author', 'title', 'data',)

        

