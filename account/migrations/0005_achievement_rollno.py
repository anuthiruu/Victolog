# Generated by Django 4.2.4 on 2023-09-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_achievement"),
    ]

    operations = [
        migrations.AddField(
            model_name="achievement",
            name="rollno",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
