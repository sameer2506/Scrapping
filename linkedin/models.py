from django.db import models


class LinkedInProfile(models.Model):
    fullName = models.CharField(max_length=250)
    jobTitle = models.CharField(max_length=250)
    linkedInUrl = models.CharField(max_length=250)
    status = models.CharField(max_length=250, null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(null=True)
