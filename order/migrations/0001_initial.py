# Generated by Django 5.2.1 on 2025-05-19 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                (
                    "quantity",
                    models.PositiveIntegerField(default=1, verbose_name="数量"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("waiting", "等待"), ("finished", "结束")],
                        default="waiting",
                        max_length=10,
                        verbose_name="状态",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="book.bookinfo",
                        verbose_name="书籍",
                    ),
                ),
            ],
        ),
    ]
