from django.forms import ModelForm, ChoiceField, CharField, MultipleChoiceField
from .models import Post, Author, Category
from django.forms.widgets import Textarea, CheckboxSelectMultiple


CHOICE_CATEGORY = []
for name in Category.objects.all().values('id', 'name'):
    CHOICE_CATEGORY.append((name.get('id'), name.get('name')))


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        auth = [(0, 'Выберите имя')]
        for names in Author.objects.all().order_by('user__username').values('id', 'user__username'):
            auth.append((names.get('id'), names.get('user__username')))
        self.fields['author'].choices = auth

        choice = []
        for names in Category.objects.all().values('id', 'name'):
            choice.append((names.get('id'), names.get('name')))
        self.fields['category'].choices = choice

    author = ChoiceField(label='Имя автора')
    type = ChoiceField(choices=Post.TYPE, label='Тип публикации')
    head = CharField(max_length=255, empty_value='Без названия', label='Заголовок')
    text = CharField(empty_value='Без содержания', label='Содержание', widget=Textarea)
    category = MultipleChoiceField(label='Категории', widget=CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ('author', 'type', 'head', 'text', 'category')
