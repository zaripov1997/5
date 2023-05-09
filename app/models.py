"""
Definition of models.
"""

from django.db import models

# Create your models here.
from django.contrib import admin #добавили использование административного модуля 
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin


# Модель данных Блога
class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")

    def get_absolute_url(self): # в метод возваращае строку с уникальным интернет-адресом записи
        return reverse('blogpost', args=[str(self.id)])

    def __str__(self): # метод возвращает название, используемое для представления отдельных записей
        return self.title

    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе
        verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)

# Модель комментариев
class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий") 
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")

    def __str__(self):
        return "Комментарий %s к %s" % (self.author, self.post)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "Комментарий" # имя, под которым модель будет отображаться в административном разделе
        verbose_name_plural = "комментария к статьям блога" # тоже для всех статей блога

admin.site.register(Comment)

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name = "Название категории")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name = "URL")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('product_list_by_category',
                        args=[self.slug])
   


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name = "Категория продукта" )
    name = models.CharField(max_length=200, db_index=True, verbose_name = "Название продукта")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name = "URL")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    description = models.TextField(blank=True, verbose_name = "Описание продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "Цена")
    stock = models.PositiveIntegerField(verbose_name = "Запасы на складе")
    available = models.BooleanField(default=True, verbose_name = "Доступность продукта")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Дата добавления продукта")
    updated = models.DateTimeField(auto_now=True, verbose_name = "Дата изменения продукта")

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('product_detail',
                        args=[self.id, self.slug])
    










