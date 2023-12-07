from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from urllib.parse import urlencode


# Create your views here.
def index(request):
    context = {}
    return render(request, "prediction/index.html", context)


def submit_prediction(request):
    age = __age_in_days(request.POST["DOB"])
    height = __to_cm(int(request.POST["feet"]), int(request.POST["inches"]))
    weight = __pounds_to_kilograms(int(request.POST["weight"]))
    gender = __gender_to_code(request.POST["gender"])
    systolic_blood_pressure = int(request.POST["systolicBloodPressure"])
    diastolicBloodPressure = int(request.POST["diastolicBloodPressure"])
    cholesterol = __normal_to_value(request.POST["cholesterol"])
    glucose = __normal_to_value(request.POST["glucose"])
    smoking = __yes_no_to_binary(request.POST["smoking"])
    alcohol = __yes_no_to_binary(request.POST["alcohol"])
    physical = __yes_no_to_binary(request.POST["physical"])
    bmi = __get_bmi(weight, height)

    query_params = {
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "systolicBloodPressure": systolic_blood_pressure,
        "diastolicBloodPressure": diastolicBloodPressure,
        "cholesterol": cholesterol,
        "glucose": glucose,
        "smoking": smoking,
        "alcohol": alcohol,
        "physical": physical,
        "bmi": bmi,
    }

    redirect_url = "/machinelearning?" + urlencode(query_params)
    return redirect(redirect_url)


def __age_in_days(date_of_birth):
    dob_date = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
    today_date = datetime.datetime.today()
    delta = today_date - dob_date
    return delta.days


def __pounds_to_kilograms(pounds):
    return pounds * 0.453592


def __gender_to_code(gender):
    if gender == "Male":
        return 0
    else:
        return 1


def __yes_no_to_binary(value):
    if value == "Yes":
        return 1
    else:
        return 0


def __normal_to_value(normal):
    if normal == "Normal":
        return 1
    elif normal == "Above Normal":
        return 2
    else:
        return 3


def __get_bmi(kg, cm):
    meters = cm * 0.01
    meters_squared = meters**2
    return kg / meters_squared


def __to_cm(feet, inches):
    print("Feet:", feet)
    print("inches:", inches)
    return ((feet * 12) + inches) * 2.54
