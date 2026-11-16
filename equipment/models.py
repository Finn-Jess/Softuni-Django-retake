from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from core.models import TimestampedModel


class Category(TimestampedModel):
    name = models.CharField(
        max_length=60,
        unique=True,
        error_messages={
            'unique': 'A category with this name already exists in the vault.',
        },
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class GearItem(TimestampedModel):
    class ConditionChoices(models.TextChoices):
        NEW = 'NEW', 'Like New'
        GOOD = 'GOOD', 'Field Ready (Good)'
        WORN = 'WORN', 'Heavily Used (Worn)'

    serial_validator = RegexValidator(
        regex=r'^[A-Z]{2,4}-\d{3,6}$',
        message='Serial code must follow format PREFIX-NUMBER (e.g., CAM-1042 or TENT-009).',
    )

    name = models.CharField(max_length=100)
    serial_code = models.CharField(
        max_length=20,
        unique=True,
        validators=[serial_validator],
        error_messages={
            'unique': 'This serial code is already registered to another piece of gear.',
        },
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items',
    )
    condition = models.CharField(
        max_length=10,
        choices=ConditionChoices.choices,
        default=ConditionChoices.NEW,
    )
    daily_rate = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.00'), message='Daily rate must be at least €1.00.')],
    )
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0.01'), message='Weight must be greater than 0 kg.')],
    )
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def clean(self):
        super().clean()
        if self.condition == self.ConditionChoices.WORN and self.daily_rate and self.daily_rate > Decimal('250.00'):
            raise ValidationError({
                'daily_rate': 'Heavily worn equipment cannot have a daily rate above €250.00.'
            })

    @property
    def status_label(self):
        return 'Available' if self.is_available else 'Checked Out'

    def __str__(self):
        return f"{self.name} ({self.serial_code})"