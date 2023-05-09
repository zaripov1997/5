"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog
from django.contrib import admin
from .models import Category, Product



class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    ok = forms.ChoiceField(label='Понравился ли Вам наш сайт', choices=[('1','Да'),('2','Нет')],
                               widget=forms.RadioSelect, initial=1)
    gender = forms.ChoiceField(label='Сколько у вас животных', choices=[('1','1'),('2','2'),('3','3'),('4','Больше 3-х')],
                               widget=forms.RadioSelect, initial=1)
    internet= forms.ChoiceField(label='Какие у вас домашние животные',
                                 choices=(('1','Собака'),
                                          ('2','Кошка'),
                                          ('3','Попугай'),
                                          ('4','Хомяк'),
                                          ('5','Несколько животных разных видов')), initial=1)
    notice = forms.BooleanField(label='Получать новости с сайта на email', required=False)
    email = forms.EmailField(label='Ваш e-mail', min_length=7)
    message = forms.CharField(label='Ваши пожелания и вопросы', 
                              widget=forms.Textarea(attrs={'rows':12, 'cols':20}))
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка",}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

