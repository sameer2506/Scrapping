# Generated by Django 4.1.1 on 2022-10-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedInProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=250)),
                ('jobTitle', models.CharField(max_length=250)),
                ('linkedInUrl', models.CharField(max_length=250)),
                ('status', models.CharField(max_length=250, null=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('updatedOn', models.DateTimeField(null=True)),
            ],
        ),
    ]
