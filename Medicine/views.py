from django.shortcuts import render, redirect
from .models import Medicine
from Record.models import Record
import datetime as dt


def view_current_medicines(request):
    if request.user.is_authenticated:
        medicines = Medicine.objects.filter(user=request.user)
        med_count = 0
        curr_meds = []
        for med in medicines:
            if med.start_date <= dt.date.today() and med.end_date >= dt.date.today():
                med_count += 1
                curr_meds.append(med)
        context = {'medicine': curr_meds, 'heading': "Your Current Medicines"}
        return render(request, 'view_medicines.html', context)
    return redirect('/login')


def view_medicines(request):
    if request.user.is_authenticated:
        med = Medicine.objects.filter(user=request.user)
        context = {'medicine': med, 'heading': "Your Medicines"}
        return render(request, 'view_medicines.html', context)
    return redirect('/login')


def medicine(request):
    context = {}
    return render(request, 'medicine_main.html', context)


def medicine_form(request):
    user = request.user
    query_set = Record.objects.filter(patient=user)

    if request.method == "POST":
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        repeat_unit = request.POST.get('repeat_unit')
        repeat_magnitude = request.POST.get('repeat_magnitude')
        additional_info = request.POST.get('additional_info')
        record_details = request.POST.get('record')
        record = None
        if record_details != "None":
            details = record_details.split('.')
            pk = details[0]
            # record_date = details[0]
            # space = record_date.split(' ')
            # doctor_name = details[1]
            # ailment_type = details[2]

            record = Record.objects.get(pk=pk)

        print(name, start_date, end_date, repeat_unit, record)
        new_med = Medicine(user=user, name=name, start_date=start_date,
                           end_date=end_date, repeat_unit=repeat_unit,
                           repeat_magnitude=repeat_magnitude, additional_info=additional_info,
                           record=record)
        new_med.save()

        return redirect('/medicine/view/')

    return render(request, "medicine_form.html", {'records': query_set})


def delete_medicine(request, pk):
    med = Medicine.objects.get(pk=pk)
    med.delete()
    return redirect('/medicine/view/')
