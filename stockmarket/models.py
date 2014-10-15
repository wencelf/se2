from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Investor(User):
	cash = models.PositiveIntegerField(default=10, null=True)
	phone = models.IntegerField(null=True)
	twitter = models.CharField(max_length=100, null=True)
	imagen = models.ImageField(upload_to='photos',max_length=500, default='', null=True)
	imgurl = models.URLField(max_length=500, default='', null=True)
	testfield = models.CharField(max_length=100, null=True)
	def __unicode__(self):
		return str(self.email)
        
class Startup(models.Model):
	startupName = models.CharField(max_length=100)
	ceo = models.ForeignKey(Investor)
	askingPrice = models.PositiveIntegerField(null=True, default=1)
	last_price = models.PositiveIntegerField(null=True, default=1)
	minPrice = models.PositiveIntegerField(null=True, default=1)
	def __unicode__(self):
	    return str(self.startupName)
    
class Bank(models.Model): 
    buyer = models.ForeignKey(Investor)
    seller = models.ForeignKey(Startup)
    shares = models.DecimalField(max_digits=4, decimal_places=0)
    timeStamp = models.DateField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=0)
    
    def __unicode__(self):
        return str(self.pk)   