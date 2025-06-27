from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Kullanıcıyı kaydeder
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesap oluşturuldu: {username}')
            return redirect('register')  # Şimdilik aynı sayfaya geri dönüyoruz
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
