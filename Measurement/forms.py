from django import forms
from .models import MeasurementGroup, Measurement


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['date', 'magnitude']

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', '')
    #     super(MeasurementForm, self).__init__(*args, **kwargs)
    #     self.fields['group'] = forms.ModelChoiceField(queryset=MeasurementGroup.objects.filter(user=user))


class MeasurementGroupForm(forms.ModelForm):
    class Meta:
        model = MeasurementGroup
        fields = ['name', 'unit', 'lower_bound', 'upper_bound']

