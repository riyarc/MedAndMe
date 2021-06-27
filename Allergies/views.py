from django.shortcuts import render, redirect, HttpResponse
from .models import Allergy
from .forms import AllergyForm


def add_allergy(request):
    user = request.user
    if request.method == "POST":
        form = AllergyForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            cause = form.cleaned_data.get('cause')
            symptoms = form.cleaned_data.get('symptoms')
            medicine = form.cleaned_data.get('medicine')
            additional_notes = form.cleaned_data.get('additional_notes')

            a = Allergy(user=user, description=description, cause=cause, symptoms=symptoms, additional_notes=additional_notes,
                        medicine=medicine)
            a.save()

            return redirect('/allergy/view/')
        else:
            return HttpResponse('<h2>Form Invalid!<h2>')
    else:
        return render(request, "Allergies/allergy_form.html", {'form': AllergyForm()})


def view_allergy(request):
    allergy = Allergy.objects.filter(user=request.user)
    count = allergy.count()
    return render(request, "Allergies/view-allergy.html", {'allergy': allergy, 'count': count})


def allergy_main(request):
    return render(request, "Allergies/allergy_main.html", {})


def delete_allergy(request, pk):
    if request.user.is_authenticated:
        allergy = Allergy.objects.get(pk=pk)
        if allergy.user == request.user:
            allergy.delete()
            return redirect('/allergy/view/')
        else:
            return redirect('/allergy/view/')
    return redirect('/login')
