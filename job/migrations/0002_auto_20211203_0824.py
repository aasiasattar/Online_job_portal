# Generated by Django 3.2.9 on 2021-12-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuser',
            name='company',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentuser',
            name='status',
            field=models.CharField(max_length=30, null=True),
        ),
    ]