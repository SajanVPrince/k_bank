# Generated by Django 5.1.6 on 2025-02-14 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='balance',
            field=models.IntegerField(default=0.0),
            preserve_default=False,
        ),
    ]
