# Generated by Django 4.2 on 2023-04-15 03:34

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
            name='MicrosoftSSOUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microsoft_id', models.CharField(blank=True, max_length=255, null=True)),
                ('picture_raw', models.BinaryField(blank=True, null=True)),
                ('locale', models.CharField(blank=True, max_length=5, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Microsoft SSO User',
                'db_table': 'microsoft_sso_user',
            },
        ),
    ]