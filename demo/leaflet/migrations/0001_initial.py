# Generated by Django 5.0.4 on 2024-04-27 15:26

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InteractivePointField",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        help_text="Use map widget to point the location", srid=4326
                    ),
                ),
                (
                    "location_has_default",
                    django.contrib.gis.db.models.fields.PointField(
                        default=django.contrib.gis.geos.point.Point(-104.7703, 39.7392),
                        srid=4326,
                    ),
                ),
                (
                    "location_optional",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
            ],
            options={
                "verbose_name": "Interactive PointField",
                "verbose_name_plural": "Interactive PointField",
            },
        ),
    ]
