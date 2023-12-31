# Generated by Django 4.1.7 on 2023-10-13 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectG', '0002_groceryitem_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='grocerylist',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_lists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grocerylist',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
