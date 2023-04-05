import datetime


from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from shareshack.models import Item

class DateInput(forms.DateInput):
    input_type = 'date'

class RenewItemForm(forms.Form):
    renewal_date = forms.DateField(widget=forms.DateInput(), help_text="Enter a date between now and 4 weeks (YYYY-MM-DD).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
class TransactionForm(ModelForm):
    class Meta:
        model = Item
        fields = ['writtenId','name', 'borrower','due_back', 'condition']
        help_texts = {
            'due_back': 'Press X for returns',
            'condition': 'e.g. 10/12/18 small crack on rim',
            'borrower': 'select "-----" for returns',
        }
        widgets = {
            'due_back': DateInput(),
            'writtenId' : forms.HiddenInput(),
            'name' : forms.HiddenInput(),
        }
        