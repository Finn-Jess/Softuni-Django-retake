from django import forms
from .models import Category, GearItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Category Name',
            'description': 'Equipment Scope & Notes',
        }
        help_texts = {
            'name': 'Enter a distinct category name (e.g., Alpine Tents, Cinema Lenses).',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Optical & Camera Gear',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what types of equipment belong in this category...',
            }),
        }
        error_messages = {
            'name': {
                'required': 'Please provide a category name before saving.',
                'max_length': 'Category name cannot exceed 60 characters.',
            }
        }


class GearItemCreateForm(forms.ModelForm):
    class Meta:
        model = GearItem
        exclude = ['created_at', 'updated_at']
        labels = {
            'name': 'Equipment Name',
            'serial_code': 'Asset Serial Code',
            'category': 'Equipment Category',
            'condition': 'Physical Condition',
            'daily_rate': 'Daily Rental Rate (€)',
            'weight_kg': 'Pack Weight (kg)',
            'is_available': 'Ready for immediate deployment',
            'notes': 'Inspection & Maintenance Notes',
        }
        help_texts = {
            'serial_code': 'Format: 2–4 uppercase letters, hyphen, 3–6 digits (e.g., CAM-2048).',
            'daily_rate': 'Minimum rate is €1.00 per day.',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Sony FX3 Cinema Line'}),
            'serial_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CAM-1001'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'daily_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.50', 'placeholder': '45.00'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.05', 'placeholder': '1.25'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Included batteries, lens caps, or wear notes...'}),
        }
        error_messages = {
            'name': {'required': 'Equipment name is mandatory.'},
            'category': {'required': 'You must assign this item to a category.'},
        }


class GearItemEditForm(GearItemCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required read-only/disabled field demonstration
        self.fields['serial_code'].disabled = True
        self.fields['serial_code'].help_text = 'Asset serial codes are locked after initial registration.'


class GearFilterForm(forms.Form):
    SORT_CHOICES = [
        ('name', 'Name (A–Z)'),
        ('-name', 'Name (Z–A)'),
        ('daily_rate', 'Daily Rate (Low to High)'),
        ('-daily_rate', 'Daily Rate (High to Low)'),
        ('-created_at', 'Newest First'),
    ]

    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name or serial...',
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    condition = forms.ChoiceField(
        choices=[('', 'All Conditions')] + list(GearItem.ConditionChoices.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='name',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )