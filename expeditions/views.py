from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ExpeditionForm
from .models import Expedition


class ExpeditionListView(ListView):
    model = Expedition
    template_name = 'expeditions/expedition_list.html'
    context_object_name = 'expeditions'

    def get_queryset(self):
        queryset = Expedition.objects.annotate(gear_count=Count('assigned_gear')).order_by('start_date')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        context['status_choices'] = Expedition.StatusChoices.choices
        return context


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = 'expeditions/expedition_detail.html'
    context_object_name = 'expedition'

    def get_queryset(self):
        return Expedition.objects.prefetch_related('assigned_gear__category')


class ExpeditionCreateView(CreateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = 'expeditions/expedition_form.html'
    success_url = reverse_lazy('expeditions:expedition_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Plan New Expedition'
        context['submit_label'] = 'Create Expedition'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Expedition "{form.instance.title}" scheduled.')
        return super().form_valid(form)


class ExpeditionUpdateView(UpdateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = 'expeditions/expedition_form.html'

    def get_success_url(self):
        return reverse_lazy('expeditions:expedition_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit Expedition: {self.object.title}'
        context['submit_label'] = 'Update Expedition'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Expedition "{form.instance.title}" updated.')
        return super().form_valid(form)


class ExpeditionDeleteView(DeleteView):
    model = Expedition
    template_name = 'expeditions/expedition_confirm_delete.html'
    context_object_name = 'expedition'
    success_url = reverse_lazy('expeditions:expedition_list')

    def form_valid(self, form):
        messages.warning(self.request, f'Expedition "{self.object.title}" has been cancelled and deleted.')
        return super().form_valid(form)