# Generated by Django 3.2.7 on 2021-09-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='coupon_value',
            new_name='coupon_percentage_value',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='abandoned',
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_active',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
