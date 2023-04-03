from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import sqlite3
import pandas as pd
import json
import numpy as np

def Start_View(request):
	return render(request, 'Home.html')

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'Signup.html', {'form': form})    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('Start_View')
        else:
            return render(request, 'Signup.html', {'form': form})

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('Start_View')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello {user.username}! You have been logged in")
                return redirect('Start_View')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = AuthenticationForm() 
    return render(request,"Signin.html",{'form': form})

@login_required
def sign_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("Start_View")

def schedule(request):
    if not request.user.is_authenticated:
        messages.error(request, f"Пожалуйста , зарегистрируйтесь чтобы продолжить работу")
        return redirect('Start_View')
    if request.user.is_staff != True:
        messages.error(request, f"Вы не имеете доступа чтобы редактировать рассписание")
        return redirect('Start_View')
    else:
        conn = sqlite3.connect("db.sqlite3")
        Groups = pd.read_sql("SELECT * FROM Groups_ALL",conn)
        json_records = Groups.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data' : data}
        return render(request, 'Schedule.html', context)
def confirm(request):
    if request.method == 'POST':
        time = request.POST.getlist("time")
        groups = request.POST.getlist("groups")
        subject = request.POST.getlist("subject")
        room = request.POST.getlist("room")
        capacity = request.POST.getlist("capacity")
        day = request.POST.getlist("day")
        data={'Time':time,'Groups':groups,'Subject':subject,'Room':room,'Capacity':capacity,'Day':day}
        Group_Upload = pd.DataFrame(data)
        Group_Upload = Group_Upload.replace('',np.nan,regex=True)
        if Group_Upload.isnull().values.any() == True:
            messages.error(request, f"No correct data")
            return redirect("schedule")
        for i in range(len(Group_Upload.index)):
            check_letter = Group_Upload.iloc[i]['Subject']
            check_room = Group_Upload.iloc[i]['Room']
            if (check_letter == "Русский язык" and check_room != str(1)) or (check_letter == "Математика" and check_room != str(2)) or (check_letter == "История" and check_room != str(3)):
                messages.error(request, f"Неверно указана аудитория для предмета, Русский язык аудитория 1, Математика аудитория 2, История аудитория 3")
                return redirect("schedule")
            if check_letter != str("Русский язык") and check_letter != str("Математика") and check_letter != str("История"):
                messages.error(request, f"Неверно прописан предмет, пропишите предмет правильно")
                return redirect("schedule")               
        if Group_Upload.duplicated(subset=['Time','Subject','Room','Capacity','Day']).any() == True:
            messages.error(request, f"Мы не можем изменить текущие расписание потому что в этот день преподаватель занят для другого предмета")
            return redirect("schedule")
        conn = sqlite3.connect("db.sqlite3")
        Group_Upload.to_sql('Groups_ALL', conn, if_exists='replace', index = False)
        messages.success(request, f"Data was successfully uploaded")
        return redirect("Start_View")

def groupsone(request):
    conn = sqlite3.connect("db.sqlite3")
    Groups = pd.read_sql("SELECT * FROM Groups_ALL",conn)
    Groups = Groups.loc[Groups['Groups'] == "1"]
    Groups_Mon = Groups.loc[Groups['Day'] == "Понедельник"]
    Groups_Mon = Groups_Mon[['Time','Subject']]
    json_records = Groups_Mon.reset_index().to_json(orient ='records')
    monday = []
    monday = json.loads(json_records)
    Groups_Tus = Groups.loc[Groups['Day'] == "Вторник"]
    Groups_Tus = Groups_Tus[['Time','Subject']]
    json_records = Groups_Tus.reset_index().to_json(orient ='records')
    tusday = []
    tusday = json.loads(json_records)
    Groups_Wed = Groups.loc[Groups['Day'] == "Среда"]
    Groups_Wed = Groups_Wed[['Time','Subject']]
    json_records = Groups_Wed.reset_index().to_json(orient ='records')
    wednesday = []
    wednesday = json.loads(json_records)
    Groups_Trus = Groups.loc[Groups['Day'] == "Четверг"]
    Groups_Trus = Groups_Trus[['Time','Subject']]
    json_records = Groups_Trus.reset_index().to_json(orient ='records')
    trusday = []
    trusday = json.loads(json_records)
    Groups_Frid = Groups.loc[Groups['Day'] == "Пятница"]
    Groups_Frid = Groups_Frid[['Time','Subject']]
    json_records = Groups_Frid.reset_index().to_json(orient ='records')
    friday = []
    friday = json.loads(json_records)
    Groups_Sat = Groups.loc[Groups['Day'] == "Суббота"]
    Groups_Sat = Groups_Sat[['Time','Subject']]
    json_records = Groups_Sat.reset_index().to_json(orient ='records')
    sat = []
    sat = json.loads(json_records)
    context = {'monday' : monday, 'tusday':tusday, 'wednesday': wednesday, 'trusday':trusday, 'friday':friday, 'sat':sat}
    return render(request, 'Groups.html',context)

def groupstwo(request):
    conn = sqlite3.connect("db.sqlite3")
    Groups = pd.read_sql("SELECT * FROM Groups_ALL",conn)
    Groups = Groups.loc[Groups['Groups'] == "2"]
    Groups_Mon = Groups.loc[Groups['Day'] == "Понедельник"]
    Groups_Mon = Groups_Mon[['Time','Subject']]
    json_records = Groups_Mon.reset_index().to_json(orient ='records')
    monday = []
    monday = json.loads(json_records)
    Groups_Tus = Groups.loc[Groups['Day'] == "Вторник"]
    Groups_Tus = Groups_Tus[['Time','Subject']]
    json_records = Groups_Tus.reset_index().to_json(orient ='records')
    tusday = []
    tusday = json.loads(json_records)
    Groups_Wed = Groups.loc[Groups['Day'] == "Среда"]
    Groups_Wed = Groups_Wed[['Time','Subject']]
    json_records = Groups_Wed.reset_index().to_json(orient ='records')
    wednesday = []
    wednesday = json.loads(json_records)
    Groups_Trus = Groups.loc[Groups['Day'] == "Четверг"]
    Groups_Trus = Groups_Trus[['Time','Subject']]
    json_records = Groups_Trus.reset_index().to_json(orient ='records')
    trusday = []
    trusday = json.loads(json_records)
    Groups_Frid = Groups.loc[Groups['Day'] == "Пятница"]
    Groups_Frid = Groups_Frid[['Time','Subject']]
    json_records = Groups_Frid.reset_index().to_json(orient ='records')
    friday = []
    friday = json.loads(json_records)
    Groups_Sat = Groups.loc[Groups['Day'] == "Суббота"]
    Groups_Sat = Groups_Sat[['Time','Subject']]
    json_records = Groups_Sat.reset_index().to_json(orient ='records')
    sat = []
    sat = json.loads(json_records)
    context = {'monday' : monday, 'tusday':tusday, 'wednesday': wednesday, 'trusday':trusday, 'friday':friday, 'sat':sat}
    return render(request, 'Groups.html',context)
    
def groupsthree(request):
    conn = sqlite3.connect("db.sqlite3")
    Groups = pd.read_sql("SELECT * FROM Groups_ALL",conn)
    Groups = Groups.loc[Groups['Groups'] == "3"]
    Groups_Mon = Groups.loc[Groups['Day'] == "Понедельник"]
    Groups_Mon = Groups_Mon[['Time','Subject']]
    json_records = Groups_Mon.reset_index().to_json(orient ='records')
    monday = []
    monday = json.loads(json_records)
    Groups_Tus = Groups.loc[Groups['Day'] == "Вторник"]
    Groups_Tus = Groups_Tus[['Time','Subject']]
    json_records = Groups_Tus.reset_index().to_json(orient ='records')
    tusday = []
    tusday = json.loads(json_records)
    Groups_Wed = Groups.loc[Groups['Day'] == "Среда"]
    Groups_Wed = Groups_Wed[['Time','Subject']]
    json_records = Groups_Wed.reset_index().to_json(orient ='records')
    wednesday = []
    wednesday = json.loads(json_records)
    Groups_Trus = Groups.loc[Groups['Day'] == "Четверг"]
    Groups_Trus = Groups_Trus[['Time','Subject']]
    json_records = Groups_Trus.reset_index().to_json(orient ='records')
    trusday = []
    trusday = json.loads(json_records)
    Groups_Frid = Groups.loc[Groups['Day'] == "Пятница"]
    Groups_Frid = Groups_Frid[['Time','Subject']]
    json_records = Groups_Frid.reset_index().to_json(orient ='records')
    friday = []
    friday = json.loads(json_records)
    Groups_Sat = Groups.loc[Groups['Day'] == "Суббота"]
    Groups_Sat = Groups_Sat[['Time','Subject']]
    json_records = Groups_Sat.reset_index().to_json(orient ='records')
    sat = []
    sat = json.loads(json_records)
    context = {'monday' : monday, 'tusday':tusday, 'wednesday': wednesday, 'trusday':trusday, 'friday':friday, 'sat':sat}
    return render(request, 'Groups.html',context)