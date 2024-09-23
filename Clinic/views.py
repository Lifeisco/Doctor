from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Clinic.models import Appointment, Doctor, UserPhone
from django.contrib.auth.models import User
import datetime

#TODO Наш слот по времени считается занятым если на него записаны ко всем врачам
#TODO На слот при записи на какое то время нам предлагаются те врачи, которые не заняты

def login_page(request):
    if request.method == 'POST':

        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Сама проверка, есть ли пользователь в БД

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            error_message = 'Неверное имя пользователя или пароль'

    return render(request, 'log_in.html')


def reg_page(request):
    if request.method == 'POST':
        new_user = User.objects.create_user(request.POST.get("name"), request.POST.get("email"), request.POST.get("password"))
        new_user.save()
        phone = UserPhone.objects.create(phone_number=request.POST.get('phone'), user=new_user)
        phone.save()

    return render(request, 'register.html')


def log_out(request):
    logout(request)
    return redirect('/')


def home(request):
    return render(request, 'home.html')


import datetime


def show_table(request):
    minutes = 9 * 60
    fillTimeAndDate = []
    time_list = []
    dates = {}
    fill_time = []

    for i in range(22):
        time_list.append({"string": f"{minutes // 60}:{minutes % 60 if minutes % 60 else '00'}",
                          "minutes": minutes}) # string - строка со временем(9:00, 9:30..)  minutes - кол-во минут
        minutes += 30

    year, week, dow = datetime.datetime.now().isocalendar()
    todaysDate = datetime.date.today()  # Дата сегоднешнего дня в формате YYYY-MM-DD

    next = int(request.GET.get("next", 0)) # Переменная переключающая отображения таблицы на сл недели

    back = next
    back -= 1

    for i in range(1 - dow + next * 7, 8 - dow + next * 7):  # Цикл создания дат на неделю
        dates[(todaysDate + datetime.timedelta(days=i)).strftime("%d-%m-%Y")] = []  # Создание пустых списков дат

    appointment_data = Appointment.objects.filter(date__gte=todaysDate + datetime.timedelta(days=1 - dow + next * 7),
                                                  date__lte=todaysDate + datetime.timedelta(days=8 - dow + next * 7))

    for x in appointment_data:
        x.date = x.date.strftime("%d-%m-%Y")

        fillTimeAndDate.append({"date": x.date, "time": x.time})  # Добавление в список занятых дат и часов
        dates[x.date].append(x.time.strftime("%H:%M"))

    for dateandtime in fillTimeAndDate:
        fill_time.append(str(list(dateandtime.values())[1])[:5])

    now_time = datetime.datetime.now().time()
    now_time = now_time.minute + now_time.hour * 60
    data = {'time_list': time_list,
            'appointments': fillTimeAndDate,
            'dates': dates,
            'now_time': now_time,
            'todaysDate': todaysDate.strftime("%d-%m-%Y"),
            'fill_time': fill_time,
            'page': next + 1,
            'back': back}
    return render(request, 'table.html', context=data)


def appointment_page(request):
    date = request.GET.get("date", False)
    time = request.GET.get("time", False)

    if request.method == "POST":


        date = request.POST.get("date", False)
        time = request.POST.get("time", False)
        doctor_id = request.POST.get("doctor_id", False)
        if date and time and doctor_id:
            date = datetime.datetime.strptime(date, "%d-%m-%Y")

            appointment = Appointment()
            appointment.date = date
            appointment.time = time
            appointment.client_id = request.user
            appointment.doctor_id = Doctor.objects.get(id=doctor_id)

            appointment.save()
            date = datetime.datetime.strftime(date, "%d-%m-%Y")

    data = {
        'date': date,
        'time': time,
        'doctors': Doctor.objects.all()
    }
    return render(request, 'appointment_page.html', context=data)

def for_doctor(request):
    next = int(request.GET.get('next', 0))


    today = datetime.datetime.now().date() + datetime.timedelta(days=next)
    appoinments = Appointment.objects.filter(date=today).order_by('time')
    data = {
        'appointments': appoinments,
        'next': next+1,
        'back': next-1

    }
    return render(request, 'For_doctor.html', context=data)
