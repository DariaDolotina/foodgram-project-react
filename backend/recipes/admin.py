from django.contrib import admin


from .models import Ingredient, Follow, Recipe, Tag
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'password', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email', 'first_name')
    empty_value_display = '-пусто-'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'measure')
    list_filter = ('title', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'get_ingredients')
    search_fields = ('title', 'author')
    list_filter = ('author', 'title', 'tag')
    empty_value_display = '-пусто-'

    def get_ingredients(self):
        return "\n".join([p.ingredients for p in self.ingredient.all()])

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'code', 'slug')
    search_fields = ('pk', 'name')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'
