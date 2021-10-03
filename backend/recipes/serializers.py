from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from users.models import User
from users.serializers import UserSerializer

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class RecipeForAnonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'cooking_time')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientsSerializer(source='units', many=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'title', 'text', 'pic',
            'ingredients', 'tag', 'time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return obj.favorite_recipe.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return obj.shopping_cart.filter(user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientsSerializer(many=True)
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'title', 'text', 'pic',
            'ingredients', 'tag', 'time',
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        cooking_time = self.initial_data.get('cooking_time')
        if not ingredients:
            raise ValidationError('Выберите ингредиенты')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': (
                    'Значение должно быть положительным'
                )
            })
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients': (
                        'Значение должно быть положительным'
                    )
                })
            if ingredient in ingredients_set:
                raise ValidationError('Ингредиент уже добавлен')
            ingredients_set.add(ingredient)
        return data

    def validate_tags(self, tag):
        tags = self.initial_data.get('tag')
        tags_set = set()
        if not tag:
            raise ValidationError(
                "Выберите минимум один тег"
            )
        for tag in tags:
            if tag in tags_set:
                raise ValidationError('Этот тэг уже выбран')
            tags_set.add(tag)
        return tag

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if (IngredientAmount.objects.filter(
                    recipe=recipe, ingredient=ingredient_id).exists()):
                amount += F('amount')
            IngredientAmount.objects.update_or_create(
                recipe, ingredient=ingredient_id, defaults={'amount': amount})

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tag')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_recipe_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.title)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get('cooking_time',
                                                 recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.add_recipe_ingredients(ingredients, recipe)
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    def to_representation(self, recipe):
        data = RecipeWriteSerializer(
            recipe, context={'request': self.context.get('request')}
        ).data
        return data


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, following):
        if self.context.get('request').method == 'POST':
            if self.context.get('request').user == following:
                raise ValidationError('Нельзя подписаться на себя')
        return following


class FavoritesSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if ShoppingCart.objects.filter(user=user,
                                       recipe__id=recipe_id).exists():
            raise ValidationError('Рецепт уже отложен в корзину')
        return data

    def to_representation(self, obj):
        request = self.context.get('request')
        context = {'request': request}
        return ShoppingCartSerializer(obj.recipe, context=context).data
