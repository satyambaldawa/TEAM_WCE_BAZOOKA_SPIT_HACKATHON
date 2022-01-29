from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from .models import Exercise, Food
import datetime


# Create your views here.

def lauchpage(request):
    return render(request, 'foodtracker/index_landing.html')


def team(request):
    return render(request, 'foodtracker/team.html')


def shopping(request):
    return render(request, 'foodtracker/shop.html')


@login_required
def home(request):
    try:
        total_exercise = round(
            Exercise.objects.filter(user=request.user, time__date=datetime.date.today()).aggregate(Sum('calories'))[
                'calories__sum'], 2)
    except TypeError:
        total_exercise = 0
    try:
        total_food = round(
            Food.objects.filter(user=request.user, time__date=datetime.date.today()).aggregate(Sum('calories'))[
                'calories__sum'], 2)
    except TypeError:
        total_food = 0

    user_bmi = (request.user.profile.weight * 10000) / (request.user.profile.height ** 2)

    if request.user.profile.gender == 'Male':
        user_bmr = 88.362 + (13.397 * request.user.profile.weight) + (4.799 * request.user.profile.height) - (
                5.677 * request.user.profile.age)
    else:
        user_bmr = 447.593 + (9.24 * request.user.profile.weight) + (3.098 * request.user.profile.height) - (
                4.330 * request.user.profile.age)

    context = {
        'user_bmr': user_bmr,
        'user_bmi': user_bmi,
        'total_exercise': total_exercise,
        'total_food': total_food
    }
    return render(request, 'foodtracker/profile.html', context)


@login_required
def add_exercise(request):
    if request.method == "POST":
        sentence = request.POST['exercise_text']
        exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

        parameters = {
            "query": sentence,
            "gender": request.user.profile.gender.lower(),
            "weight_kg": float(request.user.profile.weight),
            "height_cm": float(request.user.profile.height),
            "age": request.user.profile.age
        }

        headers = {
            "x-app-id": "2ec7392b",
            "x-app-key": "055c1eaf612c6b78760525088e599755",
        }

        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            result = response.json()
            i = 0
            for exercise_one in result['exercises']:
                i += 1
                form = Exercise(user=request.user, exercise=exercise_one['name'], duration=exercise_one['duration_min'],
                                calories=exercise_one['nf_calories'])
                form.save()
            if i > 0:
                messages.success(request, f"Exercise adding successfully")

        else:
            messages.warning(request, f"Exercise adding failed")

        return redirect('exercise')

    return render(request, 'foodtracker/exercise_form.html')


@login_required
def add_food(request):
    if request.method == "POST":
        sentence = request.POST['food_text']
        exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/nutrients"

        parameters = {
            "query": sentence,
        }

        headers = {
            "x-app-id": "2ec7392b",
            "x-app-key": "055c1eaf612c6b78760525088e599755",
        }

        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            result = response.json()
            print(result)
            i = 0
            for food_one in result['foods']:
                i += 1
                form = Food(user=request.user, food=food_one['food_name'], qty=food_one['serving_qty'],
                            unit=food_one['serving_unit'], calories=food_one['nf_calories'],
                            weight=food_one['serving_weight_grams'])
                form.save()
            if i > 0:
                messages.success(request, f"Food adding successfully")

            return redirect('food')
        else:
            messages.warning(request, f"Food adding failed")

    return render(request, 'foodtracker/food_form.html')


@login_required
def exercise_page(request):
    exercise_tables = Exercise.objects.filter(user=request.user, time__date=datetime.date.today()).order_by('-time')
    total = Exercise.objects.filter(user=request.user, time__date=datetime.date.today()).aggregate(Sum('calories'))
    labels = []
    data = []
    for exercise_t in exercise_tables:
        labels.append(exercise_t.exercise)
        data.append(exercise_t.calories)
    try:
        cal_tot = round(total['calories__sum'])

    except TypeError:
        cal_tot = 0

    if cal_tot > 400:
        status_text = f'You have burned {cal_tot - 400} calories more!! Take a break dude! 😉'
    else:
        status_text = f'You need to burn {400 - cal_tot} more! Lets Start working out.. 💪'

    context = {
        'status_text': status_text,
        'exercise_tables': exercise_tables,
        'total_exercise': cal_tot,
        'today': datetime.date.today(),
        'labels': labels,
        'data': data,
    }
    return render(request, 'foodtracker/exercise_info.html', context)


@login_required
def food_page(request):
    food_tables = Food.objects.filter(user=request.user, time__date=datetime.date.today()).order_by('-time')
    total = Food.objects.filter(user=request.user, time__date=datetime.date.today()).aggregate(Sum('calories'))
    labels = []
    data = []
    for food_t in food_tables:
        labels.append(food_t.food)
        data.append(food_t.calories)

    try:
        cal_tot = round(total['calories__sum'])

    except TypeError:
        cal_tot = 0

    if cal_tot > 1600:
        status_text = f'You have consumed {cal_tot - 1600} calories more!!☹ Workout now to control'
    else:
        status_text = f'You are {1600 - cal_tot} calories short! Grab some Food 🍟'

    context = {
        'status_text': status_text,
        'food_tables': food_tables,
        'total_food': cal_tot,
        'today': datetime.date.today(),
        'labels': labels,
        'data': data,
    }
    return render(request, 'foodtracker/food_info.html', context)
