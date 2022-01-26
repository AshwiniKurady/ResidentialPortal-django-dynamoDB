from django.db import models

# Create your models here.


class Renter(models.Model):
    renter_id = models.CharField(max_length=200)
    property_id = models.CharField(max_length=200)
    renter_name = models.CharField(max_length=200)
    renter_username = models.CharField(max_length=200)
    renter_password = models.CharField(max_length=200)
    renter_firstname = models.CharField(max_length=200)
    renter_lastname = models.CharField(max_length=200)
    renter_contactnumber = models.CharField(max_length=200)
    renter_address = models.CharField(max_length=200)
    renter_email_id = models.CharField(max_length=200)


class Landlord(models.Model):
    landlord_id = models.CharField(max_length=200)
    property_id = models.CharField(max_length=200)
    landlord_name = models.CharField(max_length=200)
    landlord_username = models.CharField(max_length=200)
    landlord_password = models.CharField(max_length=200)
    landlord_firstname = models.CharField(max_length=200)
    landlord_lastname = models.CharField(max_length=200)
    landlord_contactnumber = models.CharField(max_length=200)
    landlord_email_id = models.CharField(max_length=200)