from django import forms
from .models import Medicine, Timing
from Record.models import Record


class MedicineForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(2019, 2025)]))
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(2019, 2025)]))

    class Meta:
        model = Medicine
        fields = ['name', 'start_date', 'end_date', 'repeat_unit', 'repeat_magnitude', 'additional_info']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(MedicineForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Record.objects.filter(user=user))
