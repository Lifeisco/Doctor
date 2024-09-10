from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Clinic.models import Appointment, Doctor, UserPhone
from django.contrib.auth.models import User
import datetime


#TODO Выбор специалиста (доктора)
#TODO Страница для персонала(показать записи на конкр день в формате время, имя, телефон, имя врача)
#TODO При просмотре сл недель, кнопка для переключения на предыдущую (сделано)


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
        phone = UserPhone.objects.create(phone_number=request.POST.get('phone'), user=new_user)
        phone.save()

    return render(request, 'register.html')


def log_out(request):
    logout(request)
    return redirect('/')


def home(request):
    return render(request, 'home.html')


def show_table(request):
    minutes = 9 * 60
    fill_time = []
    result = []
    dates = {}

    for i in range(22):
        result.append(f"{minutes // 60}:{minutes % 60 if minutes % 60 else '00'}")
        minutes += 30

    year, week, dow = datetime.datetime.now().isocalendar()
    today = datetime.date.today() # Дата сегоднешнего дня

    next = int(request.GET.get("next", 0))

    back = next
    back -= 1

    for i in range(1 - dow+next*7, 8 - dow+next*7): # Цикл создания дат на неделю
        dates[(today + datetime.timedelta(days=i)).strftime("%d-%m-%Y")] = [] # Создание пустых списков дат

    appointment_data = Appointment.objects.filter(date__gte=today + datetime.timedelta(days=1 - dow+next*7),
                                                  date__lte=today + datetime.timedelta(days=8 - dow+next*7))

    for x in appointment_data:
        x.date = x.date.strftime("%d-%m-%Y")
        fill_time.append({"date": x.date, "time": x.time})  # Добавление в список занятых дат и часов
        dates[x.date].append(x.time.strftime("%H:%M"))

    now = datetime.datetime.now().time().strftime("%H:%M")
    data = {'time_list': result,
            'appointments': fill_time,
            'dates': dates,
            'now': now,
            'today': today.strftime("%d-%m-%Y"),
            'user': request.user.id,
            'page': next + 1,
            'back': back}
    return render(request, 'table.html', context=data)


def appointment_page(request):
    date = request.GET.get("date", False)
    time = request.GET.get("time", False)

    if request.method == "POST":

        date = request.POST.get("date", False)
        time = request.POST.get("time", False)
        if date and time:
            date = datetime.datetime.strptime(date, "%d-%m-%Y")

            appointment = Appointment()
            appointment.date = date
            appointment.time = time
            appointment.client_id = request.user
            appointment.doctor_id = Doctor.objects.get(id=1)
            appointment.save()
            date = datetime.datetime.strftime(date, "%d-%m-%Y")

    data = {
        'date': date,
        'time': time
    }
    return render(request, 'appointment_page.html', context=data)
