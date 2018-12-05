from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

now = timezone.now()
@login_required
def item_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    items = Item.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
    return render(request, 'inventory/item_list.html',
                  {'category': category,
                   'categories': categories,
                   'items': items})

@login_required
def item_new(request):
   if request.method == "POST":
       form = ItemForm(request.POST)
       if form.is_valid():
           item = form.save(commit=False)
           item.created_date = timezone.now()
           item.save()
           item = Item.objects.filter(created_date__lte=timezone.now())
           return render(request, 'inventory/item_list.html',
                         {'items': item})
   else:
       form = ItemForm()
   return render(request, 'inventory/item_new.html', {'form': form})

@login_required
def item_edit(request, pk):
   item = get_object_or_404(Item, pk=pk)
   if request.method == "POST":
       form = ItemForm(request.POST, instance=item)
       if form.is_valid():
           item = form.save(commit=False)
           item.updated_date = timezone.now()
           item.save()
           item = Item.objects.filter(created_date__lte=timezone.now())
           return render(request, 'inventory/item_list.html',
                         {'items': item})
   else:
       form = ItemForm(instance=item)
   return render(request, 'inventory/item_edit.html', {'form': form})

@login_required
def item_delete(request, pk):
   item = get_object_or_404(Item, pk=pk)
   item.delete()
   return redirect('pantry:item_list')
