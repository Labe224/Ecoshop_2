# Generated by Django 5.1.4 on 2025-03-31 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_produits', '0009_alter_produits_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produits',
            name='description',
            field=models.CharField(null=True),
        ),
    ]
