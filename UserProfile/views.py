from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Patient
from .forms import CreateUserForm
from Record.models import Record, RecordFile
from Report.models import Report, ReportFile
from Medicine.models import Medicine
from Measurement.models import Measurement, MeasurementGroup
from django.utils import timezone
import datetime as dt
from Allergies.models import Allergy
from django.db import models


def index(request):
    return render(request, "index.html", {'user': request.user})


def date_to_int(date):
    initial = 1388534400000 + 31556926000*6 - 11*3600000 + 7*60000 + 24000
    return initial + (date.day-1)*86400000 + (date.month-1)*2629743000 + (date.year-2020)*31556926000


def set_values(measurements):
    values = []
    for m in measurements:
        values.append([date_to_int(m.date.date()), float(m.magnitude)])
    return values


def set_data_for_group(grp):
    data = dict()
    data['group'] = grp
    measurements = Measurement.objects.filter(group=grp).order_by('-magnitude').reverse()
    if len(measurements) > 1:
        min_y = measurements[0].magnitude
        max_y = measurements[1].magnitude
    else:
        min_y = 0
        max_y = 0

    data['min_y'] = min_y
    data['max_y'] = max_y

    measurements = Measurement.objects.filter(group=grp).order_by('-date').reverse()
    start_date = measurements[0].date.date()
    end_date = measurements.last().date.date()

    min_x = date_to_int(start_date)
    max_x = date_to_int(end_date)

    data['min_x'] = min_x
    data['max_x'] = max_x

    values = set_values(measurements)
    data['values'] = values

    return data


def extract_data(user):
    # Extracts all measurement(groups and magnitudes) data for that user
    groups = MeasurementGroup.objects.filter(user=user).order_by('-name')
    context = dict()

    context_list = []
    for group in groups:
        print(group.name)
        context_list.append(set_data_for_group(group))

    context['group_list'] = context_list
    return context


def dashboard(request):
    # Everything is given into the template. Go to '/dashboard/' to check
    user = request.user
    if user.is_authenticated:
        records = Record.objects.filter(patient=user).order_by('-date')
        reports = Report.objects.filter(user=user)
        medicines = Medicine.objects.filter(user=user)

        med_count = 0
        curr_meds = []
        for med in medicines:
            if med.start_date <= dt.date.today() and med.end_date >= dt.date.today():
                med_count += 1
                curr_meds.append(med)
        reminders = len(curr_meds)

        grps = MeasurementGroup.objects.filter(user=user)
        measurements = []
        for grp in grps:
            m = Measurement.objects.filter(group=grp)
            arr = []
            for i in m:
                arr.append(i)
            measurements.append(arr)

        doctors = set([])
        for record in Record.objects.filter(patient=user):
            doctors.add(record.doctor_name)

        doc_count = len(doctors)
        context = extract_data(user)
        print(context)

        allergy_count = len(Allergy.objects.filter(user=user))

        recent_records = records[:3]
        # print(recent_records, "\n\n\n")

        return render(request, "dashboard1.html", {'records': records,
                                                   'reports': reports,
                                                   'medicines': medicines,
                                                   'med_count': med_count,
                                                   'measurements': measurements,
                                                   'curr_meds': curr_meds,
                                                   'reminders': reminders,
                                                   'doc_count': doc_count,
                                                   'doctors': doctors,
                                                   'context': context,
                                                   'allergy_count': allergy_count,
                                                   'recent_records': recent_records,
                                                   })

    return redirect('/login')


def sign_up(request):
    context = {}
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created')
            return redirect('login')

    context['form'] = form
    return render(request, 'sign_up.html', context)


def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # patient = Patient.objects.get_or_create(user=user, name=username, email=user.email)

            return redirect('/dashboard')
        else:
            print('None')
            messages.info(request, 'Wrong inputs')
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('/login')


def graph(request):
    context = extract_data(request.user)
    context['groups'] = MeasurementGroup.objects.filter(user=request.user)
    # print(context['groups'])
    print(context)
    return render(request, "graph.html", context)


def search_mg_by_name(request, query):
    user = request.user
    if user.is_authenticated:
        groups = MeasurementGroup.objects.filter(user=user, name__icontains=query)
        measurements = []
        for grp in groups:
            m = Measurement.objects.filter(group=grp)
            arr = []
            for i in m:
                arr.append(i)
            measurements.append(arr)

        return render(request, "view_measurements.html", {'measurements': measurements})

    return redirect('/login')


def search_in_measurement_group(request, attribute, query):
    if attribute == "Group-Name":
        return search_mg_by_name(request, query)
    return redirect('/measure/view/')


def search_allergy_by_cause(request, query):
    if request.user.is_authenticated:
        allergy = Allergy.objects.filter(user=request.user, cause__icontains=query)
        count = allergy.count()
        return render(request, "Allergies/view-allergy.html", {'allergy': allergy, 'count': count})

    return redirect('/login')


def search_allergy_by_symptoms(request, query):
    if request.user.is_authenticated:
        allergy = Allergy.objects.filter(user=request.user, symptoms__icontains=query)
        count = allergy.count()
        return render(request, "Allergies/view-allergy.html", {'allergy': allergy, 'count': count})

    return redirect('/login')


def search_in_allergy(request, attribute, query):
    if attribute == "Cause":
        return search_allergy_by_cause(request, query)
    elif attribute == "Symptoms":
        return search_allergy_by_symptoms(request, query)
    return redirect('/allergy/view/')


def search_medicine_by_name(request, query):
    if request.user.is_authenticated:
        med = Medicine.objects.filter(user=request.user, name__icontains=query)
        context = {'medicine': med}
        return render(request, 'view_medicines.html', context)
    return redirect('/login')


def search_medicine_by_date(request, start_date, end_date):
    if request.user.is_authenticated:
        med = Medicine.objects.filter(models.Q(user=request.user, start_date__range=[start_date, end_date]) |
                                      models.Q(user=request.user, end_date__range=[start_date, end_date]))
        context = {'medicine': med}
        return render(request, 'view_medicines.html', context)
    return redirect('/login')


def search_in_medicine(request, attribute, query, start_date, end_date):
    if attribute == "Medicine-Name":
        return search_medicine_by_name(request, query)
    elif attribute == "Date":
        return search_medicine_by_date(request, start_date, end_date)
    return redirect('/medicine/view/')


def search_record_by_doctor(request, query):
    user = request.user
    if user.is_authenticated:
        print("query: ", query)
        records = Record.objects.filter(patient=user, doctor_name__icontains=query)
        print(records)
        return render(request, "view_records.html", {'records': records})

    return redirect('/login')


def search_record_by_hospital(request, query):
    user = request.user
    if user.is_authenticated:
        records = Record.objects.filter(patient=user, hospital_name__icontains=query)
        # print(records)
        return render(request, "view_records.html", {'records': records})

    return redirect('/login')


def search_record_by_ailment(request, query):
    user = request.user
    if user.is_authenticated:
        records = Record.objects.filter(patient=user, ailment_type__icontains=query)
        # print(records)
        return render(request, "view_records.html", {'records': records})

    return redirect('/login')


def search_record_by_date(request, start_date, end_date):
    user = request.user
    if user.is_authenticated:
        records = Record.objects.filter(patient=user, date__range=[start_date, end_date])
        # print(records)
        return render(request, "view_records.html", {'records': records})

    return redirect('/login')


def search_in_record(request, attribute, query, start_date, end_date):
    if attribute == "Doctor-Name":
        return search_record_by_doctor(request, query)
    elif attribute == "Hospital-Name":
        return search_record_by_hospital(request, query)
    elif attribute == "Ailment-Type":
        return search_record_by_ailment(request, query)
    elif attribute == "Date":
        return search_record_by_date(request, start_date, end_date)
    return redirect('/record/view/')


def search_report_by_name(request, query):
    user = request.user
    if user.is_authenticated:
        reports = Report.objects.filter(user=user, test_name__icontains=query)
        print(reports)
        return render(request, "view_reports.html", {'reports': reports})

    return redirect('/login')


def search_report_by_date(request, start_date, end_date):
    user = request.user
    if user.is_authenticated:
        reports = Report.objects.filter(user=user, date__range=[start_date, end_date])
        print(reports)
        return render(request, "view_reports.html", {'reports': reports})

    return redirect('/login')


def search_in_report(request, attribute, query, start_date, end_date):
    if attribute == "Test-Name":
        return search_report_by_name(request, query)
    elif attribute == "Date":
        return search_report_by_date(request, start_date, end_date)
    return redirect('/report/view/')


def search(request):
    if request.method == "GET":
        model = request.GET.get('search-for')
        attribute = request.GET.get('search-by')
        query = request.GET.get('search-query')

        print(model)
        print(attribute)
        print(query)

        start_date = ""
        end_date = ""
        if attribute == "Date":
            start_date = request.GET.get('start-date')
            end_date = request.GET.get('end-date')
            print(start_date, end_date)

        if model == "MeasurementGroup":
            return search_in_measurement_group(request, attribute, query)
        elif model == "Allergy":
            return search_in_allergy(request, attribute, query)
        elif model == "Medicine":
            return search_in_medicine(request, attribute, query, start_date, end_date)
        elif model == "Record":
            return search_in_record(request, attribute, query, start_date, end_date)
        elif model == "Report":
            return search_in_report(request, attribute, query, start_date, end_date)


def search_page(request):
    return render(request, "search.html")
