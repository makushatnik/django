# Generated by Django 4.2.3 on 2023-08-19 21:26

from django.db import migrations, models
import django.db.models.deletion
import eshop.models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='order/receipts'),
        ),
        migrations.AddField(
            model_name='product',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to=eshop.models.product_preview_path),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to=eshop.models.product_image_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='eshop.product')),
            ],
        ),
    ]