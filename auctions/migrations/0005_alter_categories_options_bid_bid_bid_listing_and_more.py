# Generated by Django 4.1 on 2022-09-15 03:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=9, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='categories',
            name='name',
            field=models.CharField(choices=[('Cameras & Photo', 'Cameras & Photo'), ('Cell Phones & Accessories', 'Cell Phones & Accessories'), ('Clothing, Shoes & Accessories', 'Clothing, Shoes & Accessories'), ('Antiques', 'Antiques'), ('Collectibles', 'Collectibles'), ('Real Estate & Boats', 'Real Estate & Boats'), ('Art', 'Art'), ('Everything Else', 'Everything Else')], default=7, max_length=32),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default='', max_length=2048, verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='timestamps',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.SET_DEFAULT, to='auctions.categories'),
        ),
        migrations.AddField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.CharField(default=None, max_length=180),
        ),
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.AddField(
            model_name='listing',
            name='watcher',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
