from django.forms import Form, ModelForm, ChoiceField, CharField, MultipleChoiceField, DateTimeField, HiddenInput
from .models import Post, Author, Category
from django.forms.widgets import Textarea, CheckboxSelectMultiple, DateTimeInput


CHOICE_CATEGORY = []
for name in Category.objects.all().values('id', 'name'):
    CHOICE_CATEGORY.append((name.get('id'), name.get('name')))


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].label = 'Имя автора'
        self.fields['category'].label = 'Категории'
        # self.fields['category'].widget = CheckboxSelectMultiple
        choice = []
        for names in Category.objects.all().values('id', 'name'):
            choice.append((names.get('id'), names.get('name')))
        self.fields['category'].choices = choice

    type = ChoiceField(choices=Post.TYPE, label='Тип публикации')
    head = CharField(max_length=255, empty_value='Без названия', label='Заголовок')
    text = CharField(empty_value='Без содержания', label='Содержание', widget=Textarea)
    #category = MultipleChoiceField(label='Категории') #, widget=CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ('author', 'type', 'head', 'text', 'category',)
        widgets = {
            'author': HiddenInput()
        }
