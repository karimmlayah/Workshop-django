from django.shortcuts import render
from .forms import UserRegisterForm
from django.shortcuts import redirect

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})