# Generated by Django 3.1.7 on 2021-03-31 12:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('status', models.CharField(choices=[('PENDING', 'Pending approval'), ('WAIT', 'Wait for samples'), ('SEQUENCING', 'Sequencing'), ('ANALYSIS', 'Analysis'), ('DONE', 'Finish'), ('ERROR', 'Error'), ('ARCHIVED', 'Archived'), ('AVAILABLE', 'Data available'), ('STOP', 'Stop'), ('VALIDATED', 'Validated'), ('ONGOING', 'Ongoing'), ('COMPLETED', 'Completed'), ('SUBMITTED', 'Submitted')], default='PENDING', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='user')),
                ('organism', models.CharField(blank=True, max_length=200, null=True)),
                ('assembly', models.CharField(blank=True, max_length=200, null=True)),
                ('tissue', models.CharField(blank=True, max_length=200, null=True)),
                ('sample_number', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(384), django.core.validators.MinValueValidator(1)])),
                ('library_prep', models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=50)),
                ('quote', models.FileField(blank=True, null=True, upload_to='quotes/%Y/%m/%d/')),
                ('quote_available', models.BooleanField(blank=True, default=False, null=True)),
                ('is_accepted', models.BooleanField(blank=True, default=False, null=True)),
                ('sample_description_file', models.FileField(blank=True, null=True, upload_to='samples/%Y/%m/%d/')),
                ('application', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
