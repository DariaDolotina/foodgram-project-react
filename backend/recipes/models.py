from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from pytils.translit import slugify

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
        )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
        )
    
    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фото'
        )
    text = models.TextField(
        verbose_name='Описание', help_text='Введите текст'
    )
    ingredients = models.ManyToManyField(Ingredient, through='IngredientAmount',
        related_name='recipes', verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.DecimalField(max_digits=5, decimal_places=2,
    verbose_name='Время приготовления')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.text[:15]


class IngredientAmount(models.Model):
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(0.1)]
        )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='amounts',
        )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='amounts',)
    
    class Meta:
        auto_created = True
        verbose_name = 'Количество в рецепте'

    def __str__(self):
        return (self.ingredient.name)


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='На кого подписаны'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} добавлен в избранное {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart'
        )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart'
        )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                       name='unique_recipes_in_cart')]
        verbose_name = 'Список покупок'
