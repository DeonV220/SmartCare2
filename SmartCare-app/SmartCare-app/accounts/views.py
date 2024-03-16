from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from .forms import SignupForm, LoginForm
from django.contrib.auth.hashers import check_password
from .models import User  # Ensure this is your custom User model if you're not using Django's built-in User model
from .forms import UserForm

# Ensure you've properly configured your custom user model in settings.py with AUTH_USER_MODEL

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                # Directly save user without setting password to use set_password method later
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])  # Use set_password to handle hashing
                user.save()
                print("User saved successfully.")
                return redirect('login')
            except Exception as e:
                print(f"Error creating user: {e}")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        # Manually get the list of all users (for demonstration; in practice, use filter)
        users = User.objects.all()
        print("All users:", users.values_list('email', flat=True))  # For debugging
        
        # Attempt to find the user by email
        try:
            user = User.objects.get(email=email)  # Ensure your user model has an 'email' field
            print("Found user:", check_password(password, user.password))
            # Verify the password
            if check_password(password, user.password):
                # Manually log the user in
                print("Found user:", check_password(password, user.password))
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # Required for manual login
                auth_login(request, user)
                print("test successful")
              
                
                # Redirect based on role, similar to your existing logic
                if user.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif user.role == 'nurse':
                    return redirect('nurse_dashboard')
                elif user.role == 'patient':
                    return redirect('patient_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
            else:
                # Password is incorrect
                return render(request, 'accounts/login.html', {'form': form, 'error_message': 'Invalid email or password'})
        except User.DoesNotExist:
            # No user found with the entered email
            return render(request, 'accounts/login.html', {'form': form, 'error_message': 'Invalid email or password'})
    return render(request, 'accounts/login.html', {'form': form})

# dashboard
def doctor_dashboard(request):
    print("Entered doctor_dashboard")
    if request.user.is_authenticated:
        if request.user.role == 'docter':
            print("Authenticated as docter")
            return render(request, 'accounts/doctor_dashboard.html')
        else:
            print("Authenticated but not docter")
            return redirect('login')
    else:
        print("Not authenticated as docter")
        return redirect('login')

def nurse_dashboard(request):
    print("Entered nurse_dashboard")
    if request.user.is_authenticated:
        if request.user.role == 'nurse':
            print("Authenticated as patient")
            return render(request, 'accounts/nurse_dashboard.html')
        else:
            print("Authenticated but not nurse")
            return redirect('login')
    else:
        print("Not authenticated as nurse")
        return redirect('login')

def patient_dashboard(request):
    print("Entered patient_dashboard")
    if request.user.is_authenticated:
        if request.user.role == 'patient':
            print("Authenticated as patient")
            return render(request, 'accounts/patient_dashboard.html')
        else:
            print("Authenticated but not patient")
            return redirect('login')
    else:
        print("Not authenticated as patient")
        return redirect('login')

def admin_dashboard(request):
    print("Entered admin_dashboard")
    if request.user.is_authenticated and request.user.role == 'admin':
        # Get all users except those with the 'admin' role
        users = User.objects.exclude(role='admin')
        return render(request, 'accounts/admin_dashboard.html', {'users': users})
    else:
        return redirect('login')



# user views
from django.shortcuts import render, redirect, get_object_or_404
# update
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        # Assume you have a UserForm for handling updates
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserForm(instance=user)
    return render(request, 'accounts/update_user.html', {'form': form})
# delete
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('admin_dashboard')
    return render(request, 'accounts/delete_confirm.html', {'user_id': user_id})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Redirect to a non-restricted page to prevent any potential loop
    return redirect('login')  # Adjust this to where you want to redirect after logout
