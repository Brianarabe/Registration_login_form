from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Broker, Agent

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=17)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class BrokerRegisterForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['broker_id', 'company_name', 'license_number', 'address', 'bio', 'profile_picture']

class AgentRegisterForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['agent_id', 'license_number', 'specialization', 'bio', 'profile_picture', 'years_of_experience']