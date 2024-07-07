# Generated by Django 5.0.3 on 2024-05-04 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('female', 'Female'), ('male', 'Male')], default='male', max_length=16),
            preserve_default=False,
        ),
    ]
