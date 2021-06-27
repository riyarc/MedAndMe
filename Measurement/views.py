from django.shortcuts import render, HttpResponse, redirect
from .models import MeasurementGroup, Measurement
from .forms import MeasurementForm, MeasurementGroupForm


def new_measurement(request):
    user = request.user
    if request.method == "POST":
        date = request.POST.get('date')
        magnitude = request.POST.get('magnitude')
        group_name = request.POST.get('group')

        group = None
        if group_name != "None":
            group = MeasurementGroup.objects.get(user=user, name=group_name)

        m = Measurement(date=date, magnitude=magnitude, group=group)
        m.save()
        return redirect('/measure/view/')

    qs = MeasurementGroup.objects.filter(user=user)
    # print(qs)

    return render(request, "measurement.html", {'groups': qs})


def create_measurement_group(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        lb = request.POST.get('lower_bound')
        ub = request.POST.get('upper_bound')

        grp = MeasurementGroup(user=user, name=name, unit=unit, lower_bound=lb, upper_bound=ub)
        grp.save()

        return redirect('/measure/view/')

    return render(request, "measurement_group_form.html")


def view_measurements(request):
    # measurements: [[m1, m2, m3, ...],
    #                [n1, n2, n3, ...],
    #                ...
    #                [z1, z2, z3, ...],
    #                ]

    # every row contains measurements of one particular group
    # every column contains measurements at a particular date for that group(row)
    user = request.user
    if user.is_authenticated:
        grps = MeasurementGroup.objects.filter(user=user)
        measurements = []
        for grp in grps:
            m = Measurement.objects.filter(group=grp)
            arr = []
            for i in m:
                arr.append(i)
            measurements.append(arr)

        return render(request, "view_measurements.html", {'measurements': measurements})

    return redirect('/login')


def delete_group(request, pk):
    group = MeasurementGroup.objects.get(pk=pk)
    group.delete()
    return redirect('/measure/view/')


def delete_measurement(request, pk):
    measurement = Measurement.objects.get(pk=pk)
    measurement.delete()
    return redirect('/measure/view/')
