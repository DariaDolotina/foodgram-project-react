from django.db.models import base
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
     DownloadShoppingCart, FavoritesView, 
     FollowViewSet, IngredientsViewSet, ShoppingCartView,
     ShoppingCartView, TagsViewSet
)

router = DefaultRouter()

router.register('ingredients', views.IngredientsViewSet, basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipe')
router.register('tags', views.TagsViewSet, basename='tags')


urlpatterns = [
    path('users/<int:author_id>/subscribe/',
         FollowViewSet.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowViewSet.as_view(),
         name='subscriptions'),
    path('recipes/<int:recipe_id>/favorite/',
         FavoritesView.as_view(),
         name='favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(),
         name='shopping_cart'),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCart.as_view(), name='dowload_shopping_cart'),
    path('', include(router.urls)),
]
