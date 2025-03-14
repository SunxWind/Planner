# Generated by Django 5.1.6 on 2025-02-24 21:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(default=None)),
                ('status', models.CharField(blank=True, choices=[(None, 'select status'), ('In queue', 'In queue'), ('In progress', 'In progress'), ('Completed', 'Completed'), ('Postponed', 'Postponed')], max_length=30)),
                ('creation_date', models.DateField(default=None)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
