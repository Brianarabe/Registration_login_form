from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    is_broker = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    def __str__(self):
        return self.username

class Broker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    broker_id = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    address = models.TextField()
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='broker_profiles/', blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    agent_id = models.CharField(max_length=20, unique=True)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='agents')
    license_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='agent_profiles/', blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - Agent at {self.broker.company_name}"
    
class Property(models.Model):
    PROPERTY_TYPES = (
        ('RES', 'Residential'),
        ('COM', 'Commercial'),
        ('IND', 'Industrial'),
        ('LAN', 'Land'),
    )
    
    STATUS_CHOICES = (
        ('AVA', 'Available'),
        ('PEN', 'Pending'),
        ('SOL', 'Sold'),
        ('LEA', 'Leased'),
    )
    
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    property_type = models.CharField(max_length=3, choices=PROPERTY_TYPES)
    address = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    square_feet = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='AVA')
    listing_date = models.DateField(auto_now_add=True)
    main_image = models.ImageField(upload_to='property_images/')
    
    def __str__(self):
        return f"{self.get_property_type_display()} at {self.address}"