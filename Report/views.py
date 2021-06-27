import os

from django.conf import settings
from django.contrib.auth.models import User
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, HttpResponse
from .models import Report, ReportFile
from Record.models import Record


def add_report(request):
    user = request.user
    if request.method == "POST":
        test_name = request.POST.get('test_name')
        date = request.POST.get('date')
        details = request.POST.get('record')
        pk = details.split('.')[0]
        record = Record.objects.get(pk=pk)
        report_files = request.FILES.getlist('file')

        r = Report(user=user, test_name=test_name, date=date, record=record)
        r.save()

        for file in report_files:
            rf = ReportFile(report=r, file=file)
            rf.save()

        return redirect('/report/view/')

    qs = Record.objects.filter(patient=user)
    return render(request, "report_form.html", {'records': qs})


def view_reports(request):
    user = request.user
    if user.is_authenticated:
        reports = Report.objects.filter(user=user)
        print(reports)
        return render(request, "view_reports.html", {'reports': reports})

    return redirect('/login')


def view_report(request, pk):
    user = request.user
    if user.is_authenticated:
        report = Report.objects.get(pk=pk)
        report_files = ReportFile.objects.filter(report=report)
        report_pdf = []
        report_img = []
        for i in report_files:
            if i.file.path.find('.pdf') != -1:
                report_pdf.append(i)
            else:
                report_img.append(i)
        return render(request, "view_report.html", {'report': report, 'report_files': report_files, 'pk': pk, 'report_pdf': report_pdf, 'report_img': report_img})
    return redirect('/login')


def delete_file(request, pk):
    file = ReportFile.objects.get(pk=pk)
    report = file.report
    pk = report.pk
    file.delete()
    return redirect('/report/view/' + str(pk))


def delete_report(request, pk):
    report = Report.ojbects.get(pk=pk)
    report.delete()
    return redirect('/report/view/')


def add_files(request, pk):
    if request.method == 'POST':
        report_files = request.FILES.getlist('file')
        report = Report.objects.get(pk=pk)
        for file in report_files:
            rf = ReportFile(report=report, file=file)
            rf.save()
        return redirect('/report/view/'+str(pk) + '/')

    return render(request, 'add_report_files.html', {'pk': pk})


def view_pdf(request, file_path):
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('ot found')

