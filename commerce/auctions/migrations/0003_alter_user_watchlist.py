# Generated by Django 5.2.1 on 2025-05-20 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_user_watchlist_alter_auctionlisting_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlisted_by', to='auctions.auctionlisting'),
        ),
    ]
