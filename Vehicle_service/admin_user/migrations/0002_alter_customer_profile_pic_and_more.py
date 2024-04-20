# Generated by Django 5.0.3 on 2024-04-20 11:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/profile_pic/CustomerProfilePic/"
            ),
        ),
        migrations.AlterField(
            model_name="mechanic",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/profile_pic/MechanicProfilePic/"
            ),
        ),
    ]
