# Generated by Django 5.1.1 on 2024-11-16 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Integration", "0005_requestlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="requestlog",
            name="response_status",
            field=models.IntegerField(null=True),
        ),
    ]
