from django.shortcuts import render
import pickle
from django.conf import settings
import os
import sklearn

# Create your views here.

SYSTOLIC_NORMAL = 119
DIASTOLIC_NORMAL = 79
SYSTOLIC_ELEVATED = 129
DIASTOLIC_ELEVATED = 79
SYSTOLIC_HIGH = 130
DIASTOLIC_HIGH = 80
BMI_OVERWEIGHT = 25.0

def index(request):
    age = int(request.GET["age"])
    gender = int(request.GET["gender"])
    height = float(request.GET["height"])
    weight = float(request.GET["weight"])
    systolic_bp = int(request.GET["systolicBloodPressure"])
    diastolic_bp = int(request.GET["diastolicBloodPressure"])
    cholesterol = int(request.GET["cholesterol"])
    glucose = int(request.GET["glucose"])
    smoking = int(request.GET["smoking"])
    alcohol = int(request.GET["alcohol"])
    physical = int(request.GET["physical"])
    bmi = float(request.GET["bmi"])

    features = [[
        age,
        gender,
        height,
        weight,
        systolic_bp,
        diastolic_bp,
        cholesterol,
        glucose,
        smoking,
        alcohol,
        physical,
    ]]
    model_path = os.path.join(settings.BASE_DIR, "machinelearning", "jupyterworkspace", "model.sav")
    ml_model = pickle.load(open(model_path, "rb"))
    prediction = ml_model.predict_proba(features)
    prediction_result = round(prediction[0][1] * 100, 2)
    print("Features:")
    print(features)

    context = {}
    context["prediction_result"] = prediction_result
    if bmi >= 25.0:
        context["bmi_level_overweight"] = True
        context["alerts_rendered"] = True
    if systolic_bp > SYSTOLIC_NORMAL and systolic_bp <= SYSTOLIC_ELEVATED and diastolic_bp <= DIASTOLIC_ELEVATED:
        context["blood_pressure_warning"] = True
        context["alerts_rendered"] = True
    elif systolic_bp >= SYSTOLIC_HIGH and diastolic_bp >= DIASTOLIC_HIGH:
        context["blood_pressure_danger"] = True
        context["alerts_rendered"] = True
    if cholesterol == 3:
        context["cholesterol_danger"] = True
        context["alerts_rendered"] = True
    elif cholesterol == 2:
        context["cholesterol_warning"] = True
        context["alerts_rendered"] = True
    if glucose == 3:
        context["glucose_danger"] = True
        context["alerts_rendered"] = True
    elif glucose == 2:
        context["glucose_warning"] = True
        context["alerts_rendered"] = True
    if smoking == 1:
        context["smoking_warning"] = True
        context["alerts_rendered"] = True
    if alcohol == 1:
        context["alcohol_warning"] = True
        context["alerts_rendered"] = True
    if physical == 0:
        context["physical_warning"] = True
        context["alerts_rendered"] = True

    return render(request, "machinelearning/index.html", context)

def notebook(request):
    return render(request, "machinelearning/notebook.html")