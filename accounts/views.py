from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate , logout
from .forms import CustomUserCreationForm
import logging
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

@login_required
def user_profile(request):
    user = request.user  # Get the current logged-in user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated information
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')  # Redirect to the same page after success
    else:
        form = UserProfileForm(instance=user)  # Pre-fill the form with current user data

    return render(request, 'accounts/user_profile.html', {'form': form, 'user': user})




def user_list(request):
    # Get the search term from the request (if any)
    search_query = request.GET.get('search', '')
    
    # Filter users based on search query (you can adjust the fields you want to search)
    users = User.objects.filter(username__icontains=search_query)
    
    # Set up pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/user_list.html', {'page_obj': page_obj, 'search_query': search_query})



logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using Django's default user model
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to the dashboard or any page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('/')  # Redirect to home or any other page
        else:
            print(form.errors)
            # Collect and display all form field errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            messages.error(request, "There were some errors with your registration.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')
