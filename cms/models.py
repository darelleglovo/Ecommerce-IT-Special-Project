from django.db import models

# Create your models here.
class AboutUs(models.Model):
    about_us = models.TextField()

    def __str__(self):
        return "About us"

    class Meta:
        verbose_name = 'About us'
        verbose_name_plural = 'About us'

class ContactUs(models.Model):
    address = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=20)
    fb_link = models.CharField(max_length=60)
    fb_messenger_link = models.CharField(max_length=60)
    email = models.CharField(max_length=50)
    open_hours = models.CharField(max_length=40)


    def __str__(self):
        return "Contact us"

    class Meta:
        verbose_name = 'Contact us'
        verbose_name_plural = 'Contact us'
