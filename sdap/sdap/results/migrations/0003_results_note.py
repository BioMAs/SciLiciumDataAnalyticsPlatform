# Generated by Django 3.1.7 on 2021-04-13 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_auto_20210413_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
