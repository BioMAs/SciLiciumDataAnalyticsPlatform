import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sdap.projects.models import Project

def get_upload_path(instance, filename):

    user_type = "user"
    if instance.created_by and instance.created_by.is_superuser:
        user_type = "admin"

    path =  os.path.join("results/{}/{}/".format(instance.project.id, instance.title), filename)
    return path

class Comparison(models.Model):
    title = models.CharField(max_length=200)
    config = models.JSONField()

    def __str__(self):
        return self.title

class Results(models.Model):

 
    title = models.CharField(max_length=200)
    result_file = models.FileField(upload_to=get_upload_path,blank=True, null=True)
    root_path = models.CharField(max_length=200,blank=True, null=True)
    project = models.ForeignKey(Project,blank=True, null=True, on_delete=models.CASCADE, related_name='result_from')
    config = models.JSONField()
    note = models.TextField(blank=True, null=True)
    comparisons = models.ManyToManyField(Comparison, related_name='as_comparison', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='result_created_by')

    # Override save method to auto increment loom custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Results, self).save(*args, **kwargs)
        path =  "results/{}/{}/".format(self.project.id, self.title)
        self.root_path = path
        super(Results, self).save()

    def __str__(self):
        return self.title
