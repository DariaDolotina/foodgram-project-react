import csv

from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(
        verbose_name='Комментарий', help_text='Введите текст',
    )
    created = models.DateTimeField(
        'date published', auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

class Ingredient(models.Model):
    title = models.CharField(max_digits=200)
    quantity = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    measure = models.CharField(
        verbose_name='Ед. измерения', help_text='Выберите единицу измерения',
    )
    def get_all_products():
        items = []
        with open('EXACT FILE PATH OF YOUR CSV FILE','r') as fp:
            # You can also put the relative path of csv file
            # with respect to the manage.py file
            reader1 = csv.reader(fp, delimiter=',')
            for value in reader1:
                items.append(value)
        return items
    # class Meta:
    #     ordering = ('-created',)

    def __str__(self):
        return self.text[:15]

class Tag(models.Model):
    description = models.TextField('Description', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=200), verbose_name='Название'
    tag = models.ForeignKey(
        Tag, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='recipes', verbose_name='Тэг'
    )
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True
    )
    description = models.TextField(
        verbose_name='Описание', help_text='Введите рецепт'
    )
    ingredients = models.ManyToManyField(Ingredient, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    class Meta:
        ordering = ['-pub_date', 'author']

    def __str__(self):
        return self.text[:15]
