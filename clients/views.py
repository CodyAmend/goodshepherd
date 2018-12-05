import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.forms import inlineformset_factory
from django.db.models import Q, Sum, Count


def client_form(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           messages.success(request, 'The client is successfully registered!')
           #return render(request, 'clients/customer_form.html', {'customer': customer})
           form = CustomerForm()
       else:
            messages.add_message(request, messages.ERROR, 'Please Complete All Fields To Submit Your Registration.')
   else:
       form = CustomerForm()
       #messages.error(request, 'The registration of the client was not completed successfully!')
       # print("Else")
   return render(request, 'clients/client_form.html', {'form': form})

@login_required
def client_list(request):
    client = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'clients/client_list.html',
                 {'clients': client})

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=client)
       if form.is_valid():
           client = form.save(commit=False)
           client.updated_date = timezone.now()
           client.save()
           client = Customer.objects.filter(created_date__lte=timezone.now())
           messages.success(request, 'The client information is successfully updated!')
           return redirect('clients:client_list')
    else:
        # edit
       form = CustomerForm(instance=client)
    return render(request, 'clients/client_edit.html', {'form': form})

@login_required
def client_delete(request, pk):
   client = get_object_or_404(Customer, pk=pk)
   client.delete()
   messages.success(request, 'The client is successfully deleted!')
   return redirect('clients:client_list')

@login_required
def visit_create(request):
    VisitItemInlineFormSet = inlineformset_factory(Visit, VisitItems, fields=('quantity','item'), fk_name='visit', extra=10)
    if request.method == "POST":
       form = VisitForm(request.POST)
       if form.is_valid():
           for i in range(0, 10):
               if int(form.data['items-' + str(i) + '-quantity']) > 0:
                   inventory = get_object_or_404(Item, pk=form.data['items-' + str(i) + '-item'])
                   inventory.quantity -= int(form.data['items-' + str(i) + '-quantity'])
                   inventory.save()
           form = form.save(commit=False)
           form.created_date = timezone.now()
           form.save()
           formset = VisitItemInlineFormSet(request.POST,request.FILES, instance=form)
           if formset.is_valid():
               formset.save()
               messages.success(request, 'The visit is added!')
           return redirect('clients:visit_list')
    else:
        form = VisitForm()
        formset= VisitItemInlineFormSet()
    return render(request, 'clients/client_visit_create.html', {'form': form, 'formsets': formset})

@login_required
def visit_list(request):
    visit = Visit.objects.filter(created_date__lte=timezone.now())
    visititem = VisitItems.objects.filter()
    return render(request, 'clients/client_visit_list.html',
                 {'visits': visit, 'visititems': visititem})

@login_required
def visit_edit(request,pk):
    visit = get_object_or_404(Visit, pk=pk)
    visitItem = get_list_or_404(VisitItems, visit=pk)
    VisitItemInlineFormSet = inlineformset_factory(Visit, VisitItems, fields=('quantity','item'), fk_name='visit', extra=10)
    if request.method == "POST":
       form = VisitForm(request.POST, instance=visit)
       if form.is_valid():
           for vi in visitItem:
               pnum = int(str(vi))
               vitem = get_object_or_404(VisitItems, id=pnum)
               for i in range(0, 10):
                   if int(form.data['items-' + str(i) + '-quantity']) > 0:
                    newItem = get_object_or_404(Item, pk=int(form.data['items-' + str(i) + '-item']))
                    if str(newItem.item_name) == str(vitem.item):
                       inventory = get_object_or_404(Item, item_name=newItem.item_name)
                       inventorychange = vitem.quantity - int(form.data['items-' + str(i) + '-quantity'])
                       inventory.quantity += inventorychange
                       inventory.save()
           form = form.save(commit=False)
           form.update_date = timezone.now()
           form.save()
           formset = VisitItemInlineFormSet(request.POST,request.FILES, instance=visit)
           if formset.is_valid():
               formset.save()
               messages.success(request, 'The visit is successfully updated!')
           return redirect('clients:visit_list')
    else:
        form = VisitForm(instance=visit)
        formset= VisitItemInlineFormSet(instance=visit)
    return render(request, 'clients/client_visit_edit.html', {'form': form, 'formsets': formset})

@login_required
def visit_delete(request, pk):
   visit = get_object_or_404(Visit, pk=pk)
   visititem = get_list_or_404(VisitItems,visit=pk)
   for vi in visititem:
       pnum = int(str(vi))
       vitem = get_object_or_404(VisitItems,id=pnum)
       inventory = get_object_or_404(Item, item_name=vitem.item)
       inventory.quantity += int(vitem.quantity)
       inventory.save()
   visit.delete()
   messages.success(request, 'The visit is successfully deleted!')
   return redirect('clients:visit_list')

@login_required
def client_search(request):
    client_list = Customer.objects.all()
    client_filter = ClientFilter(request.GET, queryset=client_list)
    if request.GET.get('format') == 'Export to csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Client_Report.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Gender', 'Birth Date', 'Address', 'City', 'Zipcode', 'Phone Number', 'Employed', 'Employer', 'Family Size','Items Requested'])
        for customer in client_list:
            writer.writerow(
            [customer.first_name, customer.last_name, customer.gender, customer.birth_date, customer.address, customer.zipcode, customer.phone, customer.is_employed, customer.employer, customer.family_size, customer.items_needed])
        return response
    return render(request, 'clients/search.html', {'filter': client_filter})

@login_required
def generate_report(request):
    template = 'clients/generate_report.html'
    query_fromDate = request.GET.get('fromDate')
    query_toDate = request.GET.get('toDate')

    if query_fromDate and query_toDate:
        #retrieve all visit items where visit date is between from date and to date and picked up is true
        result_visit = VisitItems.objects.filter(
            Q(visit__created_date__gte=query_fromDate) & Q(visit__created_date__lte=query_toDate) & Q(visit__picked_up=True))

        #converting into list
        result_list = list(result_visit)

        for visit in result_list:
            for visit1 in result_list:
                #where item name is same and date is not same
                if (visit.item.item_name == visit1.item.item_name and visit.visit.created_date != visit1.visit.created_date):
                    visit.quantity += visit1.quantity #adding two  quantities
                    result_list.remove(visit1) #removing one
                    break

    else:
        result_list = VisitItems.objects.none()

    if request.GET.get('format') == 'Export to csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['Food item', 'Total No. of items in pantry', 'No. of items taken', 'Remaining no. of items in pantry'])
        for visit in result_list:
            writer.writerow(
                [visit.item.item_name, visit.item.quantity + visit.quantity, visit.quantity, visit.item.quantity])
        return response


    context = {'visits': result_list}
    return render(request, template, context)