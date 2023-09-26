from django.shortcuts import render
from .models import Customer
from .forms import UserProfileForm, ProfilePictureForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):
    user_profile = Customer.objects.get(user=request.user)

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

    return render(request, 'profile.html', {'form': form, 'profile_picture_form': profile_picture_form})