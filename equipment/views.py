from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CategoryForm, GearFilterForm, GearItemCreateForm, GearItemEditForm
from .models import Category, GearItem


class GearListView(ListView):
    model = GearItem
    template_name = 'equipment/gear_list.html'
    context_object_name = 'gear_items'

    def get_queryset(self):
        queryset = GearItem.objects.select_related('category').all()
        self.filter_form = GearFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            q = self.filter_form.cleaned_data.get('q')
            category = self.filter_form.cleaned_data.get('category')
            condition = self.filter_form.cleaned_data.get('condition')
            sort = self.filter_form.cleaned_data.get('sort') or 'name'

            if q:
                queryset = queryset.filter(
                    Q(name__icontains=q) | Q(serial_code__icontains=q)
                )
            if category:
                queryset = queryset.filter(category=category)
            if condition:
                queryset = queryset.filter(condition=condition)
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class GearDetailView(DetailView):
    model = GearItem
    template_name = 'equipment/gear_detail.html'
    context_object_name = 'gear'

    def get_queryset(self):
        return GearItem.objects.select_related('category').prefetch_related('expeditions')


class GearCreateView(CreateView):
    model = GearItem
    form_class = GearItemCreateForm
    template_name = 'equipment/gear_form.html'
    success_url = reverse_lazy('equipment:gear_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Register New Equipment'
        context['submit_label'] = 'Add to Vault'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Equipment "{form.instance.name}" registered successfully.')
        return super().form_valid(form)


class GearUpdateView(UpdateView):
    model = GearItem
    form_class = GearItemEditForm
    template_name = 'equipment/gear_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:gear_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit Equipment: {self.object.name}'
        context['submit_label'] = 'Save Changes'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Equipment "{form.instance.name}" updated.')
        return super().form_valid(form)


class GearDeleteView(DeleteView):
    model = GearItem
    template_name = 'equipment/gear_confirm_delete.html'
    context_object_name = 'gear'
    success_url = reverse_lazy('equipment:gear_list')

    def form_valid(self, form):
        messages.warning(self.request, f'Equipment "{self.object.name}" was permanently removed.')
        return super().form_valid(form)


class CategoryListView(ListView):
    model = Category
    template_name = 'equipment/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(item_count=Count('items')).order_by('name')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'equipment/category_create.html'
    success_url = reverse_lazy('equipment:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created.')
        return super().form_valid(form)