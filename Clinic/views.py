from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Clinic.models import Appointment, Doctor, UserPhone
from django.contrib.auth.models import User
import datetime

#  TODO Отобразить записи на странице ForDoctor для конкретного доктора

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





def show_table(request):
    minutes = 9 * 60
    fillTimeAndDate = []
    time_list = []
    dates = {}
    fill_time = []
    fill_date = []
    quantityOfdoctors = Doctor.objects.all().count()
    datesIndays = []


    for i in range(22):
        time_list.append({"string": f"{minutes // 60}:{minutes % 60 if minutes % 60 else '00'}",
                          "minutes": minutes})  # string - строка со временем(9:00, 9:30..)  minutes - кол-во минут
        minutes += 30

    year, week, dow = datetime.datetime.now().isocalendar()
    todaysDate = datetime.date.today()  # Дата сегоднешнего дня в формате YYYY-MM-DD

    next = int(request.GET.get("next", 0))  # Переменная переключающая отображения таблицы на сл недели

    back = next  # Переменная переключающая отображения таблицы на прошлые недели
    back -= 1

    for i in range(1 - dow + next * 7, 8 - dow + next * 7):  # Цикл создания дат на неделю
        dates[(todaysDate + datetime.timedelta(days=i)).strftime("%d-%m-%Y")] = []  # Создание пустых списков дат

    appointment_data = Appointment.objects.filter(date__gte=todaysDate + datetime.timedelta(days=1 - dow + next * 7),
                                                  date__lte=todaysDate + datetime.timedelta(days=8 - dow + next * 7))

    for x in appointment_data:
        x.date = x.date.strftime("%d-%m-%Y")

        fillTimeAndDate.append({"date": x.date, "time": x.time})  # Добавление в список словарей занятых дат и часов
        dates[x.date].append(x.time.strftime("%H:%M").lstrip('0'))

    for date in dates:
        new_list = []
        for el in set(dates[date]):
            if dates[date].count(el) >= quantityOfdoctors:
                new_list.append(el)
        dates[date] = new_list

    for el in dates:
        date_obj = datetime.datetime.strptime(el, "%d-%m-%Y")
        days_since_start_of_year = (date_obj - datetime.datetime(date_obj.year, 1, 1)).days + 1
        datesIndays.append(days_since_start_of_year)

    for dateandtime in fillTimeAndDate:
        fill_time.append(str(dateandtime['time'])[:5].lstrip('0'))

    for date in fillTimeAndDate:
        fill_date.append(date['date'])

    now_time = datetime.datetime.now().time()
    now_time = now_time.minute + now_time.hour * 60
    data = {'time_list': time_list,
            'appointments': fillTimeAndDate,
            'dates': dates,
            'now_time': now_time,
            'todaysDate': todaysDate.strftime("%d-%m-%Y"),
            'fill_time': fill_time,
            'page': next + 1,
            'back': back,
            'fill_date': fill_date,
            'datesIndays': datesIndays,
            'dayOfYear': (datetime.datetime.now() - datetime.datetime(datetime.datetime.now().year, 1, 1)).days + 1
            }
    return render(request, 'table.html', context=data)


def appointment_page(request):
    date = request.GET.get("date", False)
    time = request.GET.get("time", False)
    date2 = False
    if date:
        date2 = datetime.datetime.strptime(date, "%d-%m-%Y")


    if request.method == "POST":

        date = request.POST.get("date", False)
        time = request.POST.get("time", False)
        doctor_id = request.POST.get("doctor_id", False)
        if date and time and doctor_id:
            date2 = datetime.datetime.strptime(date, "%d-%m-%Y")

            appointment = Appointment()
            appointment.date = date2
            appointment.time = time
            appointment.client_id = request.user
            appointment.doctor_id = Doctor.objects.get(id=doctor_id)

            appointment.save()

    AppointQuery = Appointment.objects.filter(date=date2, time=time).only('id').all()
    DoctorList = Doctor.objects.exclude(appointment__in=AppointQuery)

    data = {
        'date': date,
        'time': time,
        'doctors': DoctorList
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


# Мой функция для изучения django, она не связана с проектом
def my_foo(request):
    values = {'first_name': 'Albert',
              'last_name': 'Muller',
              'age': 23,
              'address': 'Ox. Street 14'}
    data = {'Information': values}

    return render(request, 'test.html', context=data)
