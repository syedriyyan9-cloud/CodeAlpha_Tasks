from django.db import models
from django.conf import settings
# Create your models here.
class Events(models.Model):
    '''table for events'''
    event_name = models.CharField(max_length=150)
    event_venue = models.CharField(max_length=150)
    event_date = models.DateTimeField()
    event_type = models.CharField(max_length=100)
    event_details = models.TextField()

    def __str__(self):
        '''event showcase'''
        return self.event_name
    
class User_Events(models.Model):
    '''a table connecting user and events table'''
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)

class User_Registration(models.Model):
    '''submission form for event'''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=200)
    phone = models.IntegerField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)