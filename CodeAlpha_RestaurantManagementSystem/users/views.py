from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Menu, Order, Inventory, OrderItem, Table, Reservation
from .forms import OrderForm, ReservationForm, AvailabilityCheckForm
from django.utils import timezone
from datetime import datetime
from django.contrib import messages

# Create your views here.
def registration(request):
    '''sign up the user'''
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
    return render(request, 'users/profile.html')

@login_required
def menu(request):
    menu_items = Menu.objects.filter(is_available=True)
    
    if request.method == 'POST':
        form = OrderForm(menu_items, request.POST)
        if form.is_valid():
            # Create the order for logged-in user
            new_order = Order.objects.create(user=request.user, status='pending')
            insufficient_stock = []
            total_price = 0
            
            # Loop through cleaned data to build order
            for key, value in form.cleaned_data.items():
                if key.startswith('quantity_') and value > 0:
                    item_id = int(key.split('_')[1])
                    menu_item = Menu.objects.get(id=item_id)
                    
                    # Check inventory
                    inventory = Inventory.objects.get(menu_item=menu_item)
                    if inventory.quantity_available >= value:
                        # Create OrderItem (you may want to store price at order time)
                        OrderItem.objects.create(
                            order=new_order,
                            menu_item=menu_item,
                            quantity=value
                        )
                        total_price += menu_item.price * value
                        # Optionally reduce inventory here
                        inventory.quantity_available -= value
                        inventory.save()
                    else:
                        insufficient_stock.append(f"{menu_item.name} (only {inventory.quantity_available} left)")
            
            additional_notes = form.cleaned_data['additional_notes']
            
            # Save additional notes (add this field to Order model)
            new_order.total_price = total_price
            new_order.additional_notes = additional_notes
            new_order.save()
            
            if insufficient_stock:
                new_order.delete()  # Delete order if any item fails
                return render(request, 'restaurant/menu.html', {
                    'form': form, 
                    'menu_items': menu_items, 
                    'error': f"Stock issue: {', '.join(insufficient_stock)}"
                })
            
            return redirect('users:order_success')  # You need to create this URL
    
    else:
        form = OrderForm(menu_items)
    
    return render(request, 'restaurant/menu.html', {'form': form, 'menu_items': menu_items})

@login_required
def order_submitted(request):
    '''render order successful page'''
    return render(request, 'restaurant/order_success.html')

@login_required
def user_order(request):
    # Get all orders for the logged-in user, ordered by most recent first
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    
    # Optional: Prefetch order items to avoid extra database queries in template
    orders = orders.prefetch_related('orderitem_set__menu_item')
    
    return render(request, 'restaurant/user_order.html', {'orders': orders})

@login_required
def tables(request):
    """Display tables and check availability using the form"""
    form = AvailabilityCheckForm(request.GET or None)
    available_tables = Table.objects.all().order_by('table_number')
    availability_results = []
    
    if form.is_valid():
        selected_date = form.cleaned_data['date']
        selected_time = form.cleaned_data['time']
        people_count = form.cleaned_data['people']
        
        for table in available_tables:
            can_accommodate = table.capacity >= people_count
            is_reserved = False
            
            if can_accommodate:
                is_reserved = Reservation.objects.filter(
                    table=table,
                    date=selected_date,
                    time=selected_time,
                    status__in=['pending', 'confirmed']
                ).exists()
            
            availability_results.append({
                'table': table,
                'is_available': can_accommodate and not is_reserved,
                'can_accommodate': can_accommodate,
                'is_reserved': is_reserved
            })
    
    return render(request, 'restaurant/tables.html', {
        'form': form,
        'availability_results': availability_results,
    })

@login_required
def reservations(request):
    """View and create reservations using ReservationForm"""
    # Handle reservation creation
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.status = 'confirmed'  # Or 'pending' for admin approval
            reservation.save()
            messages.success(request, f'Table {reservation.table.table_number} reserved successfully')
            return redirect('users:reservations')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        # Pre-populate form with GET parameters if coming from tables page
        initial_data = {}
        if request.GET.get('table'):
            initial_data['table'] = request.GET.get('table')
        if request.GET.get('date'):
            initial_data['date'] = request.GET.get('date')
        if request.GET.get('time'):
            initial_data['time'] = request.GET.get('time')
        if request.GET.get('people'):
            initial_data['number_of_people'] = request.GET.get('people')
        form = ReservationForm(initial=initial_data, user=request.user)  # Add user here too
    
    # Get user's existing reservations
    user_reservations = Reservation.objects.filter(
        user=request.user
    ).order_by('-date', '-time').select_related('table')
    
    today = timezone.now().date()
    future_reservations = user_reservations.filter(date__gte=today, status__in=['pending', 'confirmed'])
    past_reservations = user_reservations.filter(date__lt=today) | user_reservations.filter(status='cancelled')
    
    return render(request, 'restaurant/reservations.html', {
        'form': form,
        'future_reservations': future_reservations,
        'past_reservations': past_reservations,
    })

@login_required
def cancel_reservation(request, reservation_id):
    """Cancel an existing reservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if reservation.date >= timezone.now().date() and reservation.status != 'cancelled':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, f'Reservation for Table {reservation.table.table_number} cancelled')
    else:
        messages.error(request, 'Cannot cancel past or already cancelled reservations')
    
    return redirect('users:reservations')
