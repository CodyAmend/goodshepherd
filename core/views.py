from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from .decorators import volunteer_required, administrator_required, superuser_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def about_us(request):
   return render(request, 'about_us.html',
                 {'core': about_us})

@login_required
@administrator_required
def volunteer_list(request):
    volunteer = Volunteer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'user/volunteer_list.html',
                 {'volunteers': volunteer})


@login_required
@administrator_required
def volunteer_add(request):
    if request.method == 'POST':
        user_form = VolunteerSignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            Volunteer.objects.create(user=new_user)
            messages.success(request, 'The volunteer is successfully added. Add additional information!')
            return redirect('core:volunteer_list')
    else:
        user_form = VolunteerSignUpForm()
    return render(request,
                  'user/user_add.html',
                  {'user_form': user_form})


@login_required
@administrator_required
def volunteer_edit(request,pk):
    user = get_object_or_404(User, pk=pk)
    name = user.username
    volunteer = get_object_or_404(Volunteer,user=user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=user,
                                 data=request.POST)
        profile_form = VolunteerForm(instance=volunteer,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'The volunteer is successfully updated!')
            return redirect('core:volunteer_list')
        else:
            messages.error(request, 'Error updating volunteer!')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = VolunteerForm(instance=volunteer)
    return render(request,'user/user_edit.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'name':name})

@login_required
@volunteer_required
def volunteer_profile_edit(request):
    name = request.user.username
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = VolunteerForm(instance=request.user.volunteer,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile successfully updated!')
        else:
            messages.error(request, 'Error updating your profile!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = VolunteerForm(instance=request.user.volunteer)
    return render(request,'user/user_edit.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'name': name})

@login_required
@administrator_required
def volunteer_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'The volunteer is successfully deleted!')
    return redirect('core:volunteer_list')

@login_required
@superuser_required
def administrator_list(request):
    administrator = Administrator.objects.filter(created_date__lte=timezone.now())
    return render(request, 'user/administrator_list.html',
                 {'administrators': administrator})


@login_required
@superuser_required
def administrator_add(request):
    if request.method == 'POST':
        user_form = AdministratorSignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            Administrator.objects.create(user=new_user)
            messages.success(request, 'The administrator is successfully added. Add additional information!')
            return redirect('core:administrator_list')
    else:
        user_form = AdministratorSignUpForm()
    return render(request,
                  'user/user_add.html',
                  {'user_form': user_form})

@login_required
@superuser_required
def administrator_edit(request,pk):
    user = get_object_or_404(User, pk=pk)
    name = user.username
    administrator = get_object_or_404(Administrator,user=user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=user,
                                 data=request.POST)
        profile_form = AdministratorForm(instance=administrator,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'The administrator is successfully updated!')
            return redirect('core:administrator_list')
        else:
            messages.error(request, 'Error updating user!')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = AdministratorForm(instance=administrator)
    return render(request,'user/user_edit.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'name':name})

@login_required
@administrator_required
def administrator_profile_edit(request):
    name = request.user.username
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = AdministratorForm(instance=request.user.administrator,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile successfully updated!')
        else:
            messages.error(request, 'Error updating your profile!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = AdministratorForm(instance=request.user.administrator)
    return render(request,'user/user_edit.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'name':name})

@login_required
@superuser_required
def administrator_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'The administrator is successfully deleted!')
    return redirect('core:administrator_list')

