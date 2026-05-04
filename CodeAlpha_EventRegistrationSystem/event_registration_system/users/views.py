from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Events, User_Events, User_Registration
from .forms import user_reg

# Create your views here.
def registration(request):
    '''Register user'''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form':form})

@login_required
def profile(request):
    '''user profile'''
    return render(request, 'users/profile.html',{'user':request.user})

@login_required
def event_list(request):
    registered_event_ids = User_Events.objects.filter(user_id=request.user).values_list('event_id', flat=True)
    events = Events.objects.exclude(id__in=registered_event_ids)
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_registration(request, pk):
    '''register for event'''
    event = Events.objects.get(id = pk)
    existing_reg = User_Registration.objects.filter(user_id=request.user).first()
    form = user_reg(request.POST)
    if form.is_valid():
        registration = form.save(commit=False)
        registration.user_id = request.user
        registration.save()
        User_Events.objects.create(user_id = request.user, event_id = event)
        return redirect('users:profile')
    else:
        form = user_reg(instance=existing_reg) if existing_reg else user_reg()    
    return render(request, 'events/event_registration.html', {'form':form, 'event':event})

@login_required
def my_events(request):
    '''show list of registered events'''
    user_events = User_Events.objects.filter(user_id = request.user).select_related('event_id')
    events = [ue.event_id for ue in user_events]
    return render(request, 'events/my_events.html', {'events':events})

@login_required
def cancel_registration(request, event_id):
    event = Events.objects.get(id=event_id)
    registration = User_Events.objects.get(user_id=request.user, event_id=event)
    registration.delete()
    return redirect('users:my_events')


