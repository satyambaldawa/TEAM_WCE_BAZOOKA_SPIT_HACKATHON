from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lauchpage, name='launch-page'),
    path('home/', views.home, name='home-page'),
    path('exercise-form/', views.add_exercise, name='add-exercise'),
    path('exercise/', views.exercise_page, name='exercise'),
    path('food-form/', views.add_food, name='add-food'),
    path('food/', views.food_page, name='food'),
]
