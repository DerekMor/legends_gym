from django.shortcuts import render, redirect
from .models import Customer
from .forms import UserProfileForm, ProfilePictureForm
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from products.models import Wishlist

# Create your views here.
@login_required
def profile(request):
    user_profile = Customer.objects.get(user=request.user)

    wishlist, _ = Wishlist.objects.get_or_create(customer=user_profile)

    orders = Order.objects.filter(customer=user_profile).order_by('-date')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and profile_picture_form.is_valid():
            form.save()
            profile_picture_form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
        profile_picture_form = ProfilePictureForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form, 'profile_picture_form': profile_picture_form, 'orders': orders, 'wishlist': wishlist,})