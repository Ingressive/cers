from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
import requests, json
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

states = ['ABIA', 'ADAMAWA', 'AKWA IBOM', 'ANAMBRA', 'BAUCHI', 'BAYELSA', 'BENUE', 'BORNO', 'CROSS RIVER', 'DELTA', 'EBONYI', 'EDO', 'EKITI', 'ENUGU', 'FCT', 'GOMBE', 'IMO', 'JIGAWA', 'KADUNA', 'KANO', 'KATSINA', 'KEBBI', 'KOGI', 'KWARA', 'LAGOS', 'NASARAWA', 'NIGER', 'OGUN', 'ONDO', 'OSUN', 'OYO', 'PLATEAU', 'RIVERS', 'SOKOTO', 'TARABA', 'YOBE', 'ZAMFARA']

# Temporary homepage view
def home(request):
    return render(request, 'index.html')

# Temporary map view
def mapV(request):
    return render(request, 'map.html')

# Temporary list view
def listV(request):
    return render(request, 'tables.html')

# User signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Listens to USSD webhooks data
@csrf_exempt
@require_POST
def process_listen(request):
    # Process the data from provider
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        userInput = text.split('*')
        step = len(userInput)

        response = ""
        print('Currently at step: ',step)

        if step == 1:
            response = "CON Select a State: \n"
            for s, state in enumerate(states):
                response += "{}. {} \n".format(s+1, state)
        
        elif step == 2:
            response = "CON Enter your report message: \n"

        elif step == 3:
            Report.object.create(
                number=phone_number,
                location=userInput[-2],
                message=userInput[-1]
            )
            response = "END Report successfully posted!"
                
        return HttpResponse(response)