from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, BrokerRegisterForm, AgentRegisterForm
from .models import User, Broker, Agent, Property  # Assuming you have a Property model

def home(request):
    return render(request, 'accounts/home.html')

def register_broker(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        broker_form = BrokerRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and broker_form.is_valid():
            user = user_form.save(commit=False)
            user.is_broker = True
            user.save()
            broker = broker_form.save(commit=False)
            broker.user = user
            broker.save()
            messages.success(request, 'Broker registration successful! Please login.')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        broker_form = BrokerRegisterForm()
    return render(request, 'accounts/register_broker.html', {
        'user_form': user_form,
        'broker_form': broker_form
    })

def register_agent(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        agent_form = AgentRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and agent_form.is_valid():
            user = user_form.save(commit=False)
            user.is_agent = True
            user.save()
            agent = agent_form.save(commit=False)
            agent.user = user
            agent.broker = Broker.objects.first()  # Assign to a broker - modify as needed
            agent.save()
            messages.success(request, 'Agent registration successful! Please login.')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        agent_form = AgentRegisterForm()
    return render(request, 'accounts/register_agent.html', {
        'user_form': user_form,
        'agent_form': agent_form
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_broker:
                return redirect('broker_dashboard')
            elif user.is_agent:
                return redirect('agent_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def broker_dashboard(request):
    if not request.user.is_broker:
        return redirect('home')
    properties = Property.objects.filter(broker=request.user.broker)
    agents = Agent.objects.filter(broker=request.user.broker)
    return render(request, 'accounts/broker/dashboard.html', {
        'properties': properties,
        'agents': agents
    })

@login_required
def broker_profile(request):
    if not request.user.is_broker:
        return redirect('home')
    broker = request.user.broker
    if request.method == 'POST':
        # Add profile update logic here
        pass
    return render(request, 'accounts/broker/profile.html', {'broker': broker})

@login_required
def broker_properties(request):
    if not request.user.is_broker:
        return redirect('home')
    properties = Property.objects.filter(broker=request.user.broker)
    return render(request, 'accounts/broker/properties.html', {'properties': properties})

@login_required
def broker_property_detail(request, property_id):
    if not request.user.is_broker:
        return redirect('home')
    property = get_object_or_404(Property, id=property_id, broker=request.user.broker)
    return render(request, 'accounts/broker/property_detail.html', {'property': property})

@login_required
def agent_dashboard(request):
    if not request.user.is_agent:
        return redirect('home')
    properties = Property.objects.filter(agent=request.user.agent)
    return render(request, 'accounts/agent/dashboard.html', {'properties': properties})

@login_required
def agent_profile(request):
    if not request.user.is_agent:
        return redirect('home')
    agent = request.user.agent
    if request.method == 'POST':
        # Add profile update logic here
        pass
    return render(request, 'accounts/agent/profile.html', {'agent': agent})

@login_required
def agent_properties(request):
    if not request.user.is_agent:
        return redirect('home')
    properties = Property.objects.filter(agent=request.user.agent)
    return render(request, 'accounts/agent/properties.html', {'properties': properties})

@login_required
def agent_property_detail(request, property_id):
    if not request.user.is_agent:
        return redirect('home')
    property = get_object_or_404(Property, id=property_id, agent=request.user.agent)
    return render(request, 'accounts/agent/property_detail.html', {'property': property})