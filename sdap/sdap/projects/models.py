from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import  User


class Project(models.Model):

    PROJECT_STATUS = (
        ('PENDING', 'Pending approval'),
        ('WAIT', 'Wait for samples'),
        ('SEQUENCING', 'Sequencing'),
        ('ANALYSIS', 'Analysis'),
        ('DONE', 'Finish'),
        ('ERROR', 'Error'),
        ('ARCHIVED', 'Archived'),
        ('AVAILABLE', 'Data available'),
        ('STOP', 'Stop'),
        ('VALIDATED', 'Validated'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('SUBMITTED', 'Submitted'),
    )

    LIBRARY_PREPARATION = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField("description", blank=True)
    status = models.CharField(max_length=50, choices=PROJECT_STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='project_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))
    organism = models.CharField(max_length=200, blank=True, null=True)
    assembly = models.CharField(max_length=200, blank=True, null=True)
    tissue = models.CharField(max_length=200, blank=True, null=True)
    sample_number = models.IntegerField(default=1,validators=[MaxValueValidator(384),MinValueValidator(1)])
    library_prep = models.CharField(max_length=50, choices=LIBRARY_PREPARATION, default="NO")
    quote = models.FileField(upload_to='quotes/%Y/%m/%d/', blank=True, null=True)
    quote_available = models.BooleanField(default=False, blank=True, null=True)
    application = models.CharField(max_length=200, blank=True, null=True)
    is_accepted = models.BooleanField(default=False, blank=True, null=True)
    sample_description_file = models.FileField(upload_to='samples/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.title
