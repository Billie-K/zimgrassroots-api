# Generated by Django 4.1.6 on 2023-02-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_beneficiary_options_remove_beneficiary_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='avatar',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=''),
        ),
    ]