from django.urls import include, path

from djoser import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
]
