# forms.py
from django import forms
from .models import Menu, Reservation, Table
from datetime import datetime

class OrderForm(forms.Form):
    def __init__(self, menu_items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in menu_items:
            self.fields[f'quantity_{item.id}'] = forms.IntegerField(
                initial=0,
                min_value=0,
                required=False,
                label=item.name,
                widget=forms.NumberInput(attrs={'class': 'quantity-input', 'data-item-id': item.id})
            )
    
    additional_notes = forms.CharField(widget=forms.Textarea, required=False, label='Special instructions')

class AvailabilityCheckForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    people = forms.IntegerField(min_value=1, max_value=20, label='Number of people')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'number_of_people': forms.NumberInput(attrs={'min': 1, 'max': 20}),
        }
    
    def __init__(self, *args, **kwargs):
        # Pop 'user' from kwargs BEFORE calling super()
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show tables that can accommodate the selected number of people
        if 'number_of_people' in self.data:
            try:
                people = int(self.data.get('number_of_people'))
                self.fields['table'].queryset = Table.objects.filter(capacity__gte=people)
            except (ValueError, TypeError):
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if table and date and time:
            # Check if table is already reserved at that time
            existing = Reservation.objects.filter(
                table=table,
                date=date,
                time=time,
                status__in=['pending', 'confirmed']
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing.exists():
                raise forms.ValidationError(f'Table {table.table_number} is already reserved at this date and time')
        
        return cleaned_data
