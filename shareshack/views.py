from django.shortcuts import render
from shareshack.models import Department, Item, Transaction
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

def home(request):
    string1 = 'Hi There'
    string2 = 'Goodbye'
    department_list = Department.objects.all()
    context = {
        'department_list': department_list,
        'string1': string1,
        'string2': string2
    }
    return render(request, 'home.html', context = context)

class ItemListView(generic.ListView):
    model = Item

class ItemDetailView(generic.DetailView):
    model = Item

class DepartmentDetailView(generic.DetailView):
    model = Department
    template_name ='department_items.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['department_list'] = Department.objects.all()
        return context

class LoanedItemsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing items on loan to current user."""
    model = Item
    template_name ='item_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Item.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class CheckedOutItemsListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based staff only view listing all items checked out from facility."""
    permission_required = 'shareshack.can_mark_returned'
    model = Item
    template_name ='all_checked_out_items.html'
    paginate_by = 10

    def get_queryset(self):
        return Item.objects.filter(status__exact='o').order_by('due_back')

class ItemCreate(CreateView):
    model = Item
    fields = ['department', 'writtenId', 'name', 'donor',
        'condition']  

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from shareshack.forms import RenewItemForm, TransactionForm

#Checkout/Return View
class TransactionEntry(PermissionRequiredMixin, UpdateView):
    permission_required = 'shareshack.can_mark_returned'
    template_name = "item_transaction_entry.html"

    def get(self,request,pk):
        item_obj = get_object_or_404(Item, pk=pk)
        form = TransactionForm(instance=item_obj)
        return render(request, self.template_name, {'form':form, 'item':item_obj })

    def post(self,request,pk):
        item_obj = get_object_or_404(Item, pk=pk)
        form = TransactionForm(request.POST, instance=item_obj)
        errors = None
        if form.is_valid():

            Transaction.objects.create(
                librarian = request.user,
                writtenId = form.cleaned_data.get('writtenId'),
                name = form.cleaned_data.get('name'),
                condition = form.cleaned_data.get('condition'),
                due_back = form.cleaned_data.get('due_back'),
                checked_out_to = form.cleaned_data.get('borrower'),
            )

            form.save()

            # return HttpResponseRedirect("/shareShack/items")
            return HttpResponseRedirect(reverse('index'))
        if form.errors:
            #print(form.errors)
            errors = form.errors

        context = {'form':form, 'errors':errors}
        return render(request, self.template_name, context)


#Renew View
@login_required
@permission_required('shareshack.can_mark_returned', raise_exception=True)
def renew_item_librarian(request, pk):
    """View function for renewing a specific item by librarian."""
    item_instance = get_object_or_404(Item, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewItemForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            item_instance.due_back = form.cleaned_data['renewal_date']
            item_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-checked-out-items') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewItemForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'item_instance': item_instance,
    }

    return render(request, 'item_renew_librarian.html', context)
