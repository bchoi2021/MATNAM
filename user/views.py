from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import User

def register(request):
    register_form = RegisterForm()
    context = {'forms' : register_form}

    if request.method == 'GET':
        return render(request, 'user/register.html', context)

    elif request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = User(
                user_id = register_form.user_id,
                user_pw = register_form.user_pw,
                user_name = register_form.user_name,
                user_email = register_form.user_email,
            )
            user.save()
            return redirect('/')
        else:
            context['forms'] = register_form
            if register_form.errors:
                for value in register_form.errors.values():
                 context['error'] = value
        return render(request, 'user/register.html', context)
        
def login(request):
    loginform = LoginForm()
    context = {'forms' : loginform}

    if request.method == 'GET':
        return render(request, 'user/login.html', context)

    elif request.method == 'POST':
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            request.session['login_session']=loginform.login_session
            request.session.set_expiry(0)
            return redirect('/')
        else:
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

# 팔로우
from django.shortcuts import get_object_or_404

def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(User, pk=user_pk)
        if person != request.user:
            # if request.user.followings.filter(pk=user_pk).exists():
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
            else:
                person.followers.add(request.user)
        return redirect('user:profile', person.username)
    return redirect('user:login')