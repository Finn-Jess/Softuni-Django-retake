from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimestampedModel
from equipment.models import GearItem


class Expedition(TimestampedModel):
    class StatusChoices(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        ACTIVE = 'ACTIVE', 'In the Field'
        COMPLETED = 'COMPLETED', 'Completed'

    title = models.CharField(max_length=120)
    destination = models.CharField(max_length=100)
    lead_coordinator = models.CharField(max_length=80)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
    )
    assigned_gear = models.ManyToManyField(
        GearItem,
        related_name='expeditions',
        blank=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['start_date']

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': 'Return date cannot be earlier than the departure date.'
            })

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1

    @property
    def estimated_total_cost(self):
        daily_sum = sum(item.daily_rate for item in self.assigned_gear.all())
        return daily_sum * self.duration_days

    def __str__(self):
        return f"{self.title} ({self.destination})"