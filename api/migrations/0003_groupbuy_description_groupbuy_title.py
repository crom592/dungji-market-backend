# Generated by Django 4.2.16 on 2025-02-20 02:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_user_sns_id_user_sns_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupbuy",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="groupbuy",
            name="title",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
