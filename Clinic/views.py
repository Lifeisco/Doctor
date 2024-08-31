from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Clinic.models import Appointment, Doctor
from django.contrib.auth.models import User
import datetime


#TODO Взаимодействие регистрации пользователя и записей на приём(Если не авторизован, то не запишешься на прием;
#       при записи указывается телефон из прошлой записи)
#TODO Запись на следующие недели
#TODO Выбор специалиста (доктора)
#TODO Страница для персонала(показать записи на конкр день в формате время, имя, телефон, имя врача)


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
        #new_user.is_active = False
        new_user.save()

    return render(request, 'register.html')

def log_out(request):
    logout(request)
    return redirect('/')



def home(request):
    return render(request, 'home.html')


def show_table(request):
    # request.user.is_anonymous
    minutes = 9 * 60
    fill_time = []
    result = []
    dates = []
    dates2 = {}

    for i in range(22):
        result.append(f"{minutes // 60}:{minutes % 60 if minutes % 60 else '00'}")
        minutes += 30

    year, week, dow = datetime.datetime.now().isocalendar()
    today = datetime.date.today()

    for i in range(1 - dow, 8 - dow):
        dates.append(today + datetime.timedelta(days=i))
        dates2[today + datetime.timedelta(days=i)] = []

    appointment_data = Appointment.objects.filter(date__gte=dates[0], date__lte=dates[-1])

    for x in appointment_data:
        fill_time.append({"date": x.date, "time": x.time}) # Добавление в список занятых дат и часов
        dates2[x.date].append(x.time.strftime("%H:%M"))

    now = datetime.datetime.now().time().strftime("%H:%M")
    today = datetime.date.today()
    data = {'time_list': result,
            'appointments': fill_time,
            'dates': dates,
            'dates2': dates2,
            'now': now,
            'today': today,
            'user': request.user.id}
    return render(request, 'table.html', context=data)

def appointment_page(request):
    date = request.GET.get("date", False)
    time = request.GET.get("time", False)

    if request.method == "POST":



        date = request.POST.get("date", False)
        time = request.POST.get("time", False)

        if date and time:
            date = datetime.datetime.strptime(date, "%b. %d, %Y")
            date = datetime.datetime.strftime(date, "%Y-%m-%d")

            appointment = Appointment()
            appointment.date = date
            appointment.time = time
            #appointment.client_id = client
            appointment.doctor_id = Doctor.objects.get(id=1)
            appointment.save()

    data = {
        'date': date,
        'time': time
    }
    return render(request, 'appointment_page.html', context=data)

