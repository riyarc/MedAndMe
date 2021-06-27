from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, HttpResponse
from .models import Record, RecordFile


def add_record(request):
    user = request.user
    if request.method == "POST":
        doctor_name = request.POST.get('doctor_name')
        hospital_name = request.POST.get('hospital_name')
        date = request.POST.get('date')
        ailment_type = request.POST.get('ailment_type')
        record_files = request.FILES.getlist('file')

        r = Record(patient=user, doctor_name=doctor_name,
                   hospital_name=hospital_name, date=date,
                   ailment_type=ailment_type)
        r.save()

        # print(request.FILES.getlist('file'))
        for file in record_files:
            rf = RecordFile(record=r, file=file)
            rf.save()

        # print(record)
        # print(request.FILES['file'].name, request.FILES['file'].size)
        pk = r.pk

        return redirect('/record/view/' + str(pk) + '/')

    return render(request, "record_form.html")


def view_records(request):
    user = request.user
    if user.is_authenticated:
        records = Record.objects.filter(patient=user)
        print(records)
        return render(request, "view_records.html", {'records': records})

    return redirect('/login')


def view_record(request, pk):
    user = request.user
    if user.is_authenticated:
        record = Record.objects.get(pk=pk)
        record_files = RecordFile.objects.filter(record=record)
        record_img = []
        record_pdf = []
        for file in record_files:
            if file.file.url.find('.pdf') != -1:
                record_pdf.append(file)
            else:
                record_img.append(file)
        return render(request, "view_record.html", {'record_files': record_files, 'pk': pk, 'record': record,
                                                    'record_pdf': record_pdf, 'record_img':record_img})
    return redirect('/login')


def delete_file(request, pk):
    file = RecordFile.objects.get(pk=pk)
    record = file.record
    pk = record.pk
    file.delete()
    return redirect('/record/view/' + str(pk))


def delete_record(request, pk):
    record = Record.objects.get(pk=pk)
    record.delete()
    return redirect('/record/view/')


def add_files(request, pk):
    if request.method == 'POST':
        record_files = request.FILES.getlist('file')
        record = Record.objects.get(pk=pk)
        for file in record_files:
            rf = RecordFile(record=record, file=file)
            rf.save()
        return redirect('/record/view/'+str(pk))

    return render(request, 'add_files.html', {'pk': pk})


def view_pdf(request, file_path):
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('ot found')

