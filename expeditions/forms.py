from django import forms
from equipment.models import GearItem
from .models import Expedition


class ExpeditionForm(forms.ModelForm):
    assigned_gear = forms.ModelMultipleChoiceField(
        queryset=GearItem.objects.select_related('category').all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Assign Equipment Pack',
        help_text='Select all equipment items allocated to this expedition.',
    )

    class Meta:
        model = Expedition
        exclude = ['created_at', 'updated_at']
        labels = {
            'title': 'Expedition / Shoot Title',
            'destination': 'Field Location / Region',
            'lead_coordinator': 'Lead Coordinator Name',
            'start_date': 'Departure Date',
            'end_date': 'Return Date',
            'status': 'Mission Status',
            'notes': 'Logistics & Packing Notes',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Rila Ridge Winter Documentary'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Rila Mountains, Bulgaria'}),
            'lead_coordinator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Elena Petrova'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Weather considerations, transport, or battery requirements...'}),
        }
        error_messages = {
            'title': {'required': 'Please enter a title for this expedition.'},
            'destination': {'required': 'Destination is required.'},
            'start_date': {'required': 'Please choose a departure date.'},
            'end_date': {'required': 'Please choose a return date.'},
        }