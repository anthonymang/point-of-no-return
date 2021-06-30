from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'index.html')


def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/index')
                else:
                    print('The account has been disabled.')
                    return HttpResponseRedirect('/signup')
        else:
            print('The username and/or password is incorrect.')
            return HttpResponseRedirect('/login')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

# def login_view(request):
#     if request.method is not 'POST':
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})
  
#     form = AuthenticationForm(request, request.POST)
  
#     if not form.is_valid():
#         print('-----------------------The username and/or password was incorrect')
#         return redirect('/index')
    
#     u = form.cleaned_data['username']
#     p = form.cleaned_data['password']
#     user = authenticate(username=u, password=p)

#     if not user.is_active:
#         print('The account has been disabled')
#         return redirect('/index')
    
#     login(request, user)
#     return redirect('/index')

def logout_view(request):
    logout(request)
    return redirect('/login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/index')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
