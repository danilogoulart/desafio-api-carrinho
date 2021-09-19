# Generated by Django 3.2.7 on 2021-09-19 17:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('total', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('customer_id', models.PositiveIntegerField(blank=True, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_email', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_phone', models.CharField(blank=True, max_length=11, null=True)),
                ('customer_gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('coupon_id', models.PositiveIntegerField(blank=True, null=True)),
                ('coupon_value', models.FloatField(blank=True, null=True)),
                ('abandoned', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('cart_item_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_id', models.PositiveIntegerField()),
                ('product_name', models.CharField(max_length=255)),
                ('product_sku', models.CharField(max_length=255)),
                ('product_img', models.URLField(max_length=255)),
                ('product_price', models.FloatField()),
                ('product_quantity', models.PositiveIntegerField()),
                ('total_item', models.FloatField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.cart')),
            ],
        ),
    ]