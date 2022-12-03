from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Question, TestModule, Test, UserHelper


def index(request):
    if request.user.is_authenticated:
        context = {
            'username': request.user
        }
        return render(request, 'index.html', context)
    else:
        return redirect('login')


def quiz(request):
    if request.user.is_authenticated:
        UserHelper.objects.filter(user=request.user).first().i = 0
        UserHelper.objects.filter(user=request.user).first().score = 0
        context = {
            'username': request.user,
            'title': 'Home',
            'modules': TestModule.objects.all()
        }
        return render(request, 'quiz.html', context)
    else:
        return redirect('login')


def user_registration(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                UserHelper(user=user).save()
                userhelper = UserHelper.objects.filter(user=user).first()
                userhelper.i = 0
                userhelper.score = 0
                userhelper.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("index")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = RegistrationForm()
        return render(request=request, template_name="account/register.html",
                      context={"register_form": form, 'username': request.user})
    else:
        return redirect('index')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("index")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="account/login.html",
                      context={"login_form": form, 'username': request.user})
    else:
        return redirect('index')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')


def module(request, module):
    if request.user.is_authenticated:
        userhelper = UserHelper.objects.filter(user=request.user).first()
        userhelper.i = 0
        userhelper.score = 0
        userhelper.save()
        context = {
            'username': request.user,
            'title': 'All Tests',
            'tests': Test.objects.filter(test_module__name=module).all()
        }
        return render(request, 'tests.html', context)
    else:
        return redirect('login')


def tests(request, module, test):
    if request.user.is_authenticated:
        questions = Question.objects.filter(test__name=test).all()
        userhelper = UserHelper.objects.filter(user=request.user).first()
        count = len(questions)
        if request.method == 'POST':
            if request.POST.get('variant', '') == questions[userhelper.i].answer:
                userhelper.score = userhelper.score + 1
            if userhelper.i + 1 == count:
                userhelper.save()
                return redirect('result')
            userhelper.i = userhelper.i + 1
            userhelper.save()
        try:
            context = {
                'username': request.user,
                'title': test,
                'question': questions[userhelper.i],
                'len': count,
                'i': userhelper.i + 1
            }
        except IndexError:
            context = {
                'username': request.user,
                'title': test,
                'question': ''
            }
        return render(request, 'question.html', context)
    else:
        return redirect('login')


def result(request):
    if request.user.is_authenticated:
        userhelper = UserHelper.objects.filter(user=request.user).first()
        context = {
            'username': request.user,
            'total': str(userhelper.score)+'/'+str(userhelper.i+1),
            'score': str(int((userhelper.score * 100)/(userhelper.i+1)))+ '%',
        }
        return render(request, 'result.html', context)
    else:
        return redirect('login')

